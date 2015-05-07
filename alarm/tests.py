from django.test import TestCase

from alarm.forms import AlarmForm
from alarm import client

import httpretty
import mock

import os


class NewTestCase(TestCase):
    def test_new(self):
        response = self.client.get("/alarm/new/")
        self.assertTemplateUsed(response, "alarm/new.html")
        self.assertIsInstance(response.context['form'], AlarmForm)
        self.assertFalse(response.context['form'].is_bound)

    def test_new_invalid_post(self):
        response = self.client.post("/alarm/new/", {})
        self.assertFalse(response.context['form'].is_valid())

    @mock.patch("alarm.client.list")
    @mock.patch("alarm.client.new")
    def test_new_post(self, new_mock, list_mock):
        data = {
            'name': u'name',
        }

        response = self.client.post("/alarm/new/", data)

        self.assertRedirects(response, '/alarm/')
        new_mock.assert_called_with(data)


class ListTestCase(TestCase):
    @mock.patch("alarm.client.list")
    def test_list(self, list_mock):
        response = self.client.get("/alarm/")

        self.assertTemplateUsed(response, "alarm/list.html")
        self.assertIn('list', response.context)
        list_mock.assert_called_with()


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

        client.new({})

    def test_list(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/alarm",
        )

        client.list()


class AlarmFormTestCase(TestCase):
    def test_required_fields(self):
        fields = {
            "name": True,
        }

        form = AlarmForm()

        for field, required in fields.items():
            self.assertEqual(form.fields[field].required, required)
