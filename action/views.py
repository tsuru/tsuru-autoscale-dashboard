from django.shortcuts import render, redirect

from action.forms import ActionForm
from action import client


def new(request):
    form = ActionForm(request.POST or None)

    if form.is_valid():
        client.new(form.cleaned_data)
        return redirect('/action/')

    context = {"form": form}
    return render(request, "action/new.html", context)


def list(request):
    actions = client.list().json()
    context = {
        "list": actions,
    }
    return render(request, "action/list.html", context)
