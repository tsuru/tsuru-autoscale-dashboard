from django.test import TestCase
from django.core.urlresolvers import reverse


class IndexTestCase(TestCase):
    def test_index(self):
        url = "{}?TSURU_TOKEN=bla".format(reverse("app-info", args=["app"]))
        response = self.client.get(url)
        self.assertTemplateUsed(response, "app/index.html")
