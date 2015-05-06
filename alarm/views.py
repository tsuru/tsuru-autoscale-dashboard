from django.shortcuts import render

from alarm import client


def list(request):
    alarms = client.list().json()
    context = {
        "list": alarms,
    }
    return render(request, "alarm/list.html", context)
