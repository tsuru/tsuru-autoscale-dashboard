from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from importlib import import_module

import mock


class IndexTestCase(TestCase):
    def setUp(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        self.session["tsuru_token"] = "b bla"
        self.session.save()

    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    @mock.patch("tsuru_dashboard.apps.views.AppMixin.get_app")
    @mock.patch("tsuru_autoscale.instance.client.list")
    def test_index(self, list_mock, get_app_mock, token_is_valid):
        get_app_mock.return_value = {"name": "myapp"}
        token_is_valid.return_value = True

        url = "{}".format(reverse("autoscale-app-info", args=["app"]))
        response = self.client.get(url)
        self.assertTemplateUsed(response, "app/index.html")

    @mock.patch("tsuru_dashboard.auth.views.token_is_valid")
    @mock.patch("tsuru_dashboard.apps.views.AppMixin.get_app")
    @mock.patch("tsuru_autoscale.instance.client.list")
    def test_index_instance_not_found(self, list_mock, get_app_mock, token_is_valid):
        get_app_mock.return_value = {"name": "myapp"}
        token_is_valid.return_value = True

        response_mock = mock.Mock()
        response_mock.json.return_value = None
        list_mock.return_value = response_mock

        url = "{}".format(reverse("autoscale-app-info", args=["app"]))
        response = self.client.get(url)

        self.assertTemplateUsed(response, "app/index.html")
