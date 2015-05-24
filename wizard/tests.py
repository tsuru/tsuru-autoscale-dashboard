from django.test import TestCase
from django.core.urlresolvers import reverse

from wizard import forms
from wizard import views

import mock


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
        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-index"))
        response = self.client.get(url)
        self.assertTemplateUsed(response, "wizard/index.html")

    def test_forms_prefix(self):
        url = "{}?TSURU_TOKEN=bla".format(reverse("wizard-index"))
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

        views.save_scale_up(form, token)

        alarm_mock.assert_called_with(form.cleaned_data, token)


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

        views.save_scale_down(form, token)

        alarm_mock.assert_called_with(form.cleaned_data, token)
