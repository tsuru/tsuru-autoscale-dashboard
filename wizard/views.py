from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from wizard import forms
from wizard import client


def new(request, instance=None):
    token = request.GET.get("TSURU_TOKEN")

    scale_up_form = forms.ScaleForm(request.POST or None, prefix="scale_up")
    scale_down_form = forms.ScaleForm(request.POST or None, prefix="scale_down")
    config_form = forms.ConfigForm(request.POST or None)

    if scale_up_form.is_valid() and scale_down_form.is_valid() and config_form.is_valid():
        config_data = {
            "name": instance,
            "minUnits": config_form["min"],
            "scaleUp": scale_up_form.cleaned_data,
            "scaleDown": scale_down_form.cleaned_data,
        }
        client.new(config_data, token)
        messages.success(request, u"Auto scale saved.")
        url = "{}?TSURU_TOKEN={}".format(reverse("instance-list"), token)
        return redirect(url)

    context = {
        "scale_up_form": scale_up_form,
        "scale_down_form": scale_down_form,
        "config_form": config_form,
    }

    return render(request, "wizard/index.html", context)
