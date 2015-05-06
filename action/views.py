from django.shortcuts import render

from action import client


def list(request):
    actions = client.list().json()
    context = {
        "list": actions,
    }
    return render(request, "action/list.html", context)
