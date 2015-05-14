from django.test import TestCase
from django.test.client import RequestFactory

from auth.middleware import AuthMiddleware


class TestVerifyTokenMiddleware(TestCase):
    def test_process_request_without_token(self):
        middleware = AuthMiddleware()

        request_mock = RequestFactory().get("/")
        result = middleware.process_request(request_mock)
        self.assertEqual(result.status_code, 401)

    def test_process_request(self):
        middleware = AuthMiddleware()

        request_mock = RequestFactory().get("/?TSURU_TOKEN=bla")
        result = middleware.process_request(request_mock)
        self.assertFalse(result)
        self.assertEqual(request_mock.token, "bla")
