from django.test import TestCase
from django.core.urlresolvers import reverse

import mock


class IndexTestCase(TestCase):
    @mock.patch("instance.client.list")
    def test_index(self, list_mock):
        url = "{}?TSURU_TOKEN=bla".format(reverse("app-info", args=["app"]))
        response = self.client.get(url)
        self.assertTemplateUsed(response, "app/index.html")

    @mock.patch("instance.client.list")
    def test_index_instance_not_found(self, list_mock):
        response_mock = mock.Mock()
        response_mock.json.return_value = None
        list_mock.return_value = response_mock

        url = "{}?TSURU_TOKEN=bla".format(reverse("app-info", args=["app"]))
        response = self.client.get(url)

        self.assertTemplateUsed(response, "app/index.html")
