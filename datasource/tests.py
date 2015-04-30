from django.test import TestCase

from datasource.forms import DataSourceForm


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


class DataSourceTestCase(TestCase)
