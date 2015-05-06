from django.test import TestCase

from action import client

import httpretty
import mock

import os


class ListTestCase(TestCase):
    @mock.patch("action.client.list")
    def test_list(self, list_mock):
        response = self.client.get("/action/")

        self.assertTemplateUsed(response, "action/list.html")
        self.assertIn('list', response.context)
        list_mock.assert_called_with()


class ClientTestCase(TestCase):
    def setUp(self):
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_list(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/action",
        )

        client.list()

    def test_new(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.POST,
            "http://autoscalehost.com/action",
        )

        client.new({})
