from django.shortcuts import render, redirect

from alarm.forms import AlarmForm
from alarm import client


def new(request):
    form = AlarmForm(request.POST or None)

    if form.is_valid():
        client.new(form.cleaned_data)
        return redirect('/alarm/')

    context = {"form": form}
    return render(request, "alarm/new.html", context)


def list(request):
    alarms = client.list().json()
    context = {
        "list": alarms,
    }
    return render(request, "alarm/list.html", context)
