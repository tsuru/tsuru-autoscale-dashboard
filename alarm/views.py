from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from alarm.forms import AlarmForm
from alarm import client


def new(request):
    form = AlarmForm(request.POST or None)

    if form.is_valid():
        client.new(form.cleaned_data)
        messages.success(request, u"Alarm saved.")
        return redirect(reverse('alarm-list'))

    context = {"form": form}
    return render(request, "alarm/new.html", context)


def list(request):
    alarms = client.list().json()
    context = {
        "list": alarms,
    }
    return render(request, "alarm/list.html", context)


def remove(request, name):
    client.remove(name)
    messages.success(request, u"Alarm {} removed.".format(name))
    return redirect(reverse('alarm-list'))
