from django.shortcuts import render

from instance import client


def index(request, app):
    token = request.GET.get("TSURU_TOKEN")
    instances = client.list(token).json() or []
    instance = None
    for inst in instances:
        if app in inst.get('Apps', []):
            instance = inst
    context = {
        "instance": instance,
    }
    return render(request, "app/index.html", context)
