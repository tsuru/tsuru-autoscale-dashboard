from django.http import HttpResponse


class AuthMiddleware(object):
    def process_request(self, request):
        if not request.GET.get("TSURU_TOKEN"):
            return HttpResponse(status=401)
