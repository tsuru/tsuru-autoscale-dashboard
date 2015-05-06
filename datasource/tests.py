from django.test import TestCase

from datasource.forms import DataSourceForm
from datasource import client

import httpretty

import os


class NewTestCase(TestCase):
    def test_new(self):
        response = self.client.get("/datasource/")
        self.assertTemplateUsed(response, "datasource/new.html")
        self.assertIsInstance(response.context['form'], DataSourceForm)

    def test_new_invalid_post(self):
        response = self.client.post("/datasource/", {})
        self.assertFalse(response.context['form'].is_valid())

    def test_new_post(self):
        data = {
            "url": "someurl",
            "name": "name",
            "method": "GET",
        }
        response = self.client.post("/datasource/", data)
        self.assertEquals(response.context['form'].errors, {})
        self.assertTrue(response.context['form'].is_valid())


class DataSourceTestCase(TestCase):
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
