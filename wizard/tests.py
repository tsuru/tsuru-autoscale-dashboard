from django.test import TestCase

from wizard import forms


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
