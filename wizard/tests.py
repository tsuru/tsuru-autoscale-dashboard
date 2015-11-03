from django.test import TestCase
from django.core.urlresolvers import reverse

from wizard import forms
from wizard import client

import mock
import httpretty
import os


class ScaleFormTest(TestCase):
    def test_required_fields(self):
        fields = {
            "metric": True,
            "operator": True,
            "value": True,
            "step": True,
            "wait": True,
        }

        form = forms.ScaleForm()

        for field, required in fields.items():
            self.assertEqual(form.fields[field].required, required)


class ConfigFormTest(TestCase):
    def test_required_fields(self):
        fields = {
            "min": True,
        }

        form = forms.ConfigForm()

        for field, required in fields.items():
            self.assertEqual(form.fields[field].required, required)


class IndexTestCase(TestCase):
    @mock.patch("wizard.views.process_list")
    @mock.patch("datasource.client.list")
    def test_index(self, dlist_mock, process_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-new", args=["instance"]))
        response = self.client.get(url)
        self.assertTemplateUsed(response, "wizard/index.html")

    @mock.patch("wizard.views.process_list")
    @mock.patch("datasource.client.list")
    def test_forms_prefix(self, dlist_mock, process_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-new", args=["instance"]))
        response = self.client.get(url)

        forms = {
            "scale_up_form": "scale_up",
            "scale_down_form": "scale_down",
        }

        for f, prefix in forms.items():
            self.assertEqual(response.context[f].prefix, prefix)

    @mock.patch("wizard.views.process_list")
    @mock.patch("datasource.client.list")
    def test_config_process_list(self, dlist_mock, process_mock):
        process = [("web", "web")]
        process_mock.return_value = process

        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-new", args=["instance"]))
        response = self.client.get(url)

        choices = response.context["config_form"].fields["process"].choices
        self.assertListEqual(process, choices)

    @mock.patch("wizard.views.process_list")
    @mock.patch("datasource.client.list")
    def test_scale_metrics(self, dlist_mock, process_mock):
        data = [{"Name": "cpu"}, {"Name": "mem"}]
        response_mock = mock.Mock()
        response_mock.json.return_value = data
        dlist_mock.return_value = response_mock

        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-new", args=["instance"]))
        response = self.client.get(url)

        expected_choices = [("cpu", "cpu"), ("mem", "mem")]

        choices = response.context["scale_up_form"].fields["metric"].choices
        self.assertListEqual(expected_choices, choices)

        choices = response.context["scale_down_form"].fields["metric"].choices
        self.assertListEqual(expected_choices, choices)


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
            "http://autoscalehost.com/wizard",
        )

        client.new({}, "token")

    def test_get(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/wizard/name",
        )

        client.get("name", "token")

    def test_events(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.GET,
            "http://autoscalehost.com/wizard/name/events",
        )

        client.events("name", "token")

    def test_remove(self):
        os.environ["AUTOSCALE_HOST"] = "http://autoscalehost.com"
        httpretty.register_uri(
            httpretty.DELETE,
            "http://autoscalehost.com/wizard/name",
        )

        client.remove("name", "token")


class RemoveTestCase(TestCase):
    @mock.patch("wizard.client.remove")
    def test_remove(self, remove_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-remove", args=["name"]))
        response = self.client.get(url)

        url = "{}?TSURU_TOKEN=bla".format(reverse("app-info", args=["name"]))
        self.assertIn(url, response.url)
        remove_mock.assert_called_with("name", "bla")
