from django.test import TestCase
from django.core.urlresolvers import reverse

from datasource.forms import DataSourceForm
from datasource import client

import httpretty
import mock

import os


class RemoveTestCase(TestCase):
    @mock.patch("datasource.client.list")
    @mock.patch("datasource.client.remove")
    def test_remove(self, remove_mock, list_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("datasource-remove", args=["name"]))
        response = self.client.delete(url)

        self.assertRedirects(response, reverse("datasource-list"))
        remove_mock.assert_called_with("name", "bla")


class NewTestCase(TestCase):
    def test_new(self):
        response = self.client.get(reverse("datasource-new"))
        self.assertTemplateUsed(response, "datasource/new.html")
        self.assertIsInstance(response.context['form'], DataSourceForm)
        self.assertFalse(response.context['form'].is_bound)

    def test_new_invalid_post(self):
        response = self.client.post(reverse("datasource-new"), {})
        self.assertFalse(response.context['form'].is_valid())

    @mock.patch("datasource.client.list")
    @mock.patch("datasource.client.new")
    def test_new_post(self, new_mock, list_mock):
        data = {
            'url': u'someurl',
            'body': u'',
            'headers': u'',
            'name': u'name',
            'method': u'GET',
        }

        url = "{}?TSURU_TOKEN=bla".format(reverse("datasource-new"))
        response = self.client.post(url, data)

        self.assertRedirects(response, reverse("datasource-list"))
        new_mock.assert_called_with(data, "bla")


class DataSourceListTest(TestCase):
    @mock.patch("datasource.client.list")
    def test_list(self, list_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("datasource-list"))
        response = self.client.get(url)

        self.assertTemplateUsed(response, "datasource/list.html")
        self.assertIn('list', response.context)
        list_mock.assert_called_with("bla")


class DataSourceFormTestCase(TestCase):
    def test_required_fields(self):
        fields = {
            "url": True,
            "method": True,
            "name": True,
            "body": False,
            "headers": False,
        }

        form = DataSourceForm()

        for field, required in fields.items():
            self.assertEqual(form.fields[field].required, required)


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
            "http://autoscalehost.com/datasource",
        )

        client.new({}, "token")

    def test_list(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/datasource",
        )

        client.list("token")

    def test_remove(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.DELETE,
            "http://autoscalehost.com/datasource/name",
        )

        client.remove("name", "token")

    def test_get(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/datasource/name",
            "result",
        )

        result = client.get("name", "token")
        self.assertEqual(result.text, "result")
