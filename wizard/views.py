from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from wizard import forms

from alarm import client as alarm_client


def save_scale_up(form, token):
    alarm_client.new(form.cleaned_data, token)


def save_scale_down(form, token):
    alarm_client.new(form.cleaned_data, token)


def index(request):
    token = request.GET.get("TSURU_TOKEN")

    scale_up_form = forms.ScaleForm(request.POST or None, prefix="scale_up")
    scale_down_form = forms.ScaleForm(request.POST or None, prefix="scale_down")
    config_form = forms.ConfigForm(request.POST or None)

    if scale_up_form.is_valid() and scale_down_form.is_valid() and config_form.is_valid():
        save_scale_up(scale_up_form, token)
        save_scale_down(scale_down_form, token)
        messages.success(request, u"Auto scale saved.")
        url = "{}?TSURU_TOKEN={}".format(reverse("instance-list"), token)
        return redirect(url)

    context = {
        "scale_up_form": scale_up_form,
        "scale_down_form": scale_down_form,
        "config_form": config_form,
    }

    return render(request, "wizard/index.html", context)
