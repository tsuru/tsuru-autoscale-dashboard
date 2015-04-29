from django.test import TestCase


class NewTestCase(TestCase):
    def test_new(self):
        response = self.client.get("/datasource/")
        self.assertTemplateUsed(response, "datasource/new.html")
