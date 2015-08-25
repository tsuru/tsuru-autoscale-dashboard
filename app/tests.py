from django.test import TestCase
from django.core.urlresolvers import reverse

import mock


class IndexTestCase(TestCase):
    @mock.patch("instance.client.list")
    def test_index(self, list_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("app-info", args=["app"]))
        response = self.client.get(url)
        self.assertTemplateUsed(response, "app/index.html")
