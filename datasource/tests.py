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
    def test_new_post(self, remove_mock, list_mock):
        response = self.client.delete(reverse("datasource-remove", args=["name"]))

        self.assertRedirects(response, reverse("datasource-list"))
        remove_mock.assert_called_with("name")


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

        response = self.client.post(reverse("datasource-new"), data)

        self.assertRedirects(response, reverse("datasource-list"))
        new_mock.assert_called_with(data)


class DataSourceListTest(TestCase):
    @mock.patch("datasource.client.list")
    def test_list(self, list_mock):
        response = self.client.get(reverse("datasource-list"))

        self.assertTemplateUsed(response, "datasource/list.html")
        self.assertIn('list', response.context)
        list_mock.assert_called_with()


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

        client.new({})

    def test_list(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/datasource",
        )

        client.list()

    def test_remove(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.DELETE,
            "http://autoscalehost.com/datasource/name",
        )

        client.remove(name="name")

    def test_get(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/datasource/name",
            "result",
        )

        result = client.get(name="name")
        self.assertEqual(result.text, "result")
