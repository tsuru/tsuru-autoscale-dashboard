from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from action.forms import ActionForm
from action import client


def new(request):
    form = ActionForm(request.POST or None)

    if form.is_valid():
        client.new(form.cleaned_data)
        messages.success(request, u"Action saved.")
        return redirect(reverse('action-list'))

    context = {"form": form}
    return render(request, "action/new.html", context)


def list(request):
    actions = client.list().json()
    context = {
        "list": actions,
    }
    return render(request, "action/list.html", context)
