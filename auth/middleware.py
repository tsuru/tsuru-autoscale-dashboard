from django.http import HttpResponse


class AuthMiddleware(object):
    def process_request(self, request):
        token = request.GET.get("TSURU_TOKEN")

        if hasattr(request, 'session') and not token:
            token = request.session.get('tsuru_token')

        if not token:
            return HttpResponse(status=401)

        request.token = token
