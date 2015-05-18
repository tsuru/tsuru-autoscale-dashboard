from django.test import TestCase
from django.core.urlresolvers import reverse


class IndexTest(TestCase):
    def test_index(self):
        url = "{}?TSURU_TOKEN=bla".format(reverse("index"))
        response = self.client.get(url)

        self.assertTemplateUsed(response, "index.html")
