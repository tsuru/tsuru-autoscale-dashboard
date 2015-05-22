from django.test import TestCase

from wizard import forms


class ScaleUpFormTest(TestCase):
    def test_required_fields(self):
        fields = {
            "metric": True,
            "operator": True,
            "value": True,
            "units": True,
            "wait": True,
        }

        form = forms.ScaleUpForm()

        for field, required in fields.items():
            self.assertEqual(form.fields[field].required, required)
