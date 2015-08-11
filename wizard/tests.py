from django.test import TestCase
from django.core.urlresolvers import reverse

from wizard import forms
from wizard import views
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
            "units": True,
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
    def test_index(self):
        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-new", args=["instance"]))
        response = self.client.get(url)
        self.assertTemplateUsed(response, "wizard/index.html")

    def test_forms_prefix(self):
        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-new", args=["instance"]))
        response = self.client.get(url)

        forms = {
            "scale_up_form": "scale_up",
            "scale_down_form": "scale_down",
        }

        for f, prefix in forms.items():
            self.assertEqual(response.context[f].prefix, prefix)


class SaveScaleUpTest(TestCase):
    @mock.patch("alarm.client.new")
    def test_save_scale_up(self, alarm_mock):
        data = {
            "operator": ">",
            "units": 1,
            "metric": "cpu",
            "value": 10,
            "wait": 50,
        }
        form = forms.ScaleForm(data)
        form.is_valid()
        token = "token"
        instance = "instance"

        views.save_scale_up(form, instance, token)

        expected_data = {
            "name": "scale_up_instance",
            "expression": "data.aggregations.range.buckets[0].date.buckets[0].max.value > 10",
            "enabled": True,
            "wait": 50 * 1000 * 1000 * 1000,
            "datasource": "cpu",
            "actions": ["scale_up"],
            "instance": instance,
            "envs": {"step": "1"},
        }
        alarm_mock.assert_called_with(expected_data, token)


class SaveScaleDownTest(TestCase):
    @mock.patch("alarm.client.new")
    def test_save_scale_down(self, alarm_mock):
        data = {
            "operator": ">",
            "units": 1,
            "metric": "cpu",
            "value": 10,
            "wait": 50,
        }
        form = forms.ScaleForm(data)
        form.is_valid()
        token = "token"
        instance = "instance"

        views.save_scale_down(form, instance, token)

        expected_data = {
            "name": "scale_down_instance",
            "expression": "data.aggregations.range.buckets[0].date.buckets[0].max.value > 10",
            "enabled": True,
            "wait": 50 * 1000 * 1000 * 1000,
            "datasource": "cpu",
            "actions": ["scale_down"],
            "instance": instance,
            "envs": {"step": "1"},
        }
        alarm_mock.assert_called_with(expected_data, token)


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
