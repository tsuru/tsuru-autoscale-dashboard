from django.shortcuts import render

from instance import client


def list(request):
    token = request.GET.get("TSURU_TOKEN")
    instances = client.list(token).json()
    context = {
        "list": instances,
    }
    return render(request, "instance/list.html", context)


def get(request, name):
    token = request.GET.get("TSURU_TOKEN")
    instance = client.get(name, token).json()
    alarms = client.alarms_by_instance(name, token).json()
    context = {
        "item": instance,
        "alarms": alarms,
    }
    return render(request, "instance/get.html", context)
