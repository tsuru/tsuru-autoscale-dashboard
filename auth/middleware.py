from django.http import HttpResponse


class AuthMiddleware(object):
    def process_request(self, request):
        token = request.GET.get("TSURU_TOKEN")

        if not token:
            return HttpResponse(status=401)

        request.token = token
