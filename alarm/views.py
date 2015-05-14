from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from alarm.forms import AlarmForm, datasource_list, action_list
from alarm import client


def new(request):
    token = request.GET.get("TSURU_TOKEN")

    form = AlarmForm(request.POST or None)
    form.fields['datasource'].choices = datasource_list(token)
    form.fields['actions'].choices = action_list(token)

    if form.is_valid():
        client.new(form.cleaned_data, token)
        messages.success(request, u"Alarm saved.")
        url = "{}?TSURU_TOKEN={}".format(reverse("alarm-list"), token)
        return redirect(url)

    context = {"form": form}
    return render(request, "alarm/new.html", context)


def list(request):
    token = request.GET.get("TSURU_TOKEN")
    alarms = client.list(token).json()
    context = {
        "list": alarms,
    }
    return render(request, "alarm/list.html", context)


def remove(request, name):
    token = request.GET.get("TSURU_TOKEN")
    client.remove(name, token)
    messages.success(request, u"Alarm {} removed.".format(name))
    url = "{}?TSURU_TOKEN={}".format(reverse('alarm-list'), token)
    return redirect(url)
