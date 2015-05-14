from django.test import TestCase
from django.core.urlresolvers import reverse

from alarm.forms import AlarmForm
from alarm import client

import httpretty
import mock

import os


class RemoveTestCase(TestCase):
    @mock.patch("alarm.client.list")
    @mock.patch("alarm.client.remove")
    def test_remove(self, remove_mock, list_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("alarm-remove", args=["name"]))
        response = self.client.delete(url)

        self.assertRedirects(response, reverse("alarm-list"))
        remove_mock.assert_called_with("name", "bla")


class NewTestCase(TestCase):
    @mock.patch("datasource.client")
    @mock.patch("action.client")
    def test_new(self, ds_client_mock, a_client_mock):
        response = self.client.get(reverse("alarm-new"))
        self.assertTemplateUsed(response, "alarm/new.html")
        self.assertIsInstance(response.context['form'], AlarmForm)
        self.assertFalse(response.context['form'].is_bound)

    @mock.patch("datasource.client")
    @mock.patch("action.client")
    def test_new_invalid_post(self, ds_client_mock, a_client_mock):
        response = self.client.post(reverse("alarm-new"), {})
        self.assertFalse(response.context['form'].is_valid())

    @mock.patch("action.client")
    @mock.patch("datasource.client")
    @mock.patch("alarm.client.list")
    @mock.patch("alarm.client.new")
    def test_new_post(self, new_mock, list_mock, ds_client_mock, a_client_mock):
        json_mock = mock.Mock()
        json_mock.json.return_value = [{"Name": "bla"}]
        a_client_mock.list.return_value = json_mock

        json_mock = mock.Mock()
        json_mock.json.return_value = [{"Name": "bla"}]
        ds_client_mock.list.return_value = json_mock
        data = {
            'name': u'name',
            'expression': u'x > 10',
            'enabled': True,
            'wait': 10,
            'datasource': 'bla',
            'actions': ['bla'],
        }

        url = "{}?TSURU_TOKEN=bla".format(reverse("alarm-new"))
        response = self.client.post(url, data)

        self.assertRedirects(response, reverse("alarm-list"))
        new_mock.assert_called_with(data, "bla")


class ListTestCase(TestCase):
    @mock.patch("alarm.client.list")
    def test_list(self, list_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("alarm-list"))
        response = self.client.get(url)

        self.assertTemplateUsed(response, "alarm/list.html")
        self.assertIn('list', response.context)
        list_mock.assert_called_with("bla")


class ClientTestCase(TestCase):
    def setUp(self):
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_new(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.POST,
            "http://autoscalehost.com/alarm",
        )

        client.new({}, "token")

    def test_list(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/alarm",
        )

        client.list("token")

    def test_remove(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.DELETE,
            "http://autoscalehost.com/alarm/name",
        )

        client.remove("name", "token")

    def test_get(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/alarm/name",
            "result",
        )

        result = client.get("name", "token")
        self.assertEqual(result.text, "result")


class AlarmFormTestCase(TestCase):
    def test_required_fields(self):
        fields = {
            "name": True,
            "expression": True,
            "enabled": True,
            "wait": True,
        }

        form = AlarmForm()

        for field, required in fields.items():
            self.assertEqual(form.fields[field].required, required)
