from django.test import TestCase
from django.core.urlresolvers import reverse

from instance import client

import httpretty
import mock

import os


class ListTestCase(TestCase):
    @mock.patch("instance.client.list")
    def test_list(self, list_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("instance-list"))
        response = self.client.get(url)

        self.assertTemplateUsed(response, "instance/list.html")
        self.assertIn('list', response.context)
        list_mock.assert_called_with("bla")


class GetTestCase(TestCase):
    @mock.patch("instance.client.alarms_by_instance")
    @mock.patch("instance.client.get")
    def test_get(self, list_mock, alarms_by_instance_mock):
        json_mock = mock.Mock()
        json_mock.json.return_value = {"Name": "instance"}
        list_mock.return_value = json_mock
        url = "{}?TSURU_TOKEN=bla".format(reverse("instance-get", args=["instance"]))
        response = self.client.get(url)

        self.assertTemplateUsed(response, "instance/get.html")
        self.assertIn('item', response.context)
        self.assertIn('alarms', response.context)
        self.assertIn('events', response.context)
        list_mock.assert_called_with("instance", "bla")


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
            "http://autoscalehost.com/service/instance",
        )

        client.list("token")

    def test_get(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/service/instance/name",
        )

        client.get("name", "token")

    def test_alarms_by_instance(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/alarm/instance/name",
        )

        client.alarms_by_instance("name", "token")
