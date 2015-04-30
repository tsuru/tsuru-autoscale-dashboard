from django.test import TestCase

from datasource.forms import DataSourceForm


class NewTestCase(TestCase):
    def test_new(self):
        response = self.client.get("/datasource/")
        self.assertTemplateUsed(response, "datasource/new.html")
        self.assertIsInstance(response.context['form'], DataSourceForm)
