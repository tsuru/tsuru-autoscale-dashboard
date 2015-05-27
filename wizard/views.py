from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from wizard import forms

from alarm import client as alarm_client


metrics = {
    "cpu": "data.aggregations.range.buckets[0].date.buckets[0].max.value",
    "units": "data.aggregations.range.buckets[0].date.buckets[0].unit.value",
}


def enable_alarm(form, instance, token):
    form_data = form.cleaned_data
    data = {
        "name": "enable_scale_down_{}".format(instance),
        "expression": "%s > %s" % (metrics["units"], form_data["min"]),
        "enabled": True,
        "wait": 30,
        "datasource": "units",
        "actions": ["enable_alarm"],
        "instance": instance,
        "envs": {"alarm": "scale_down_{}".format(instance)},
    }
    alarm_client.new(data, token)


def disable_alarm(form, instance, token):
    form_data = form.cleaned_data
    data = {
        "name": "disable_scale_down_{}".format(instance),
        "expression": "%s < %s" % (metrics["units"], form_data["min"]),
        "enabled": True,
        "wait": 30,
        "datasource": "units",
        "actions": ["disable_alarm"],
        "instance": instance,
        "envs": {"alarm": "scale_down_{}".format(instance)},
    }
    alarm_client.new(data, token)


def save_scale_up(form, instance, token):
    form_data = form.cleaned_data
    data = {
        "name": "scale_up_{}".format(instance),
        "expression": "%s %s %s" % (metrics["cpu"], form_data["operator"], form_data["value"]),
        "enabled": True,
        "wait": form.cleaned_data["wait"],
        "datasource": form.cleaned_data["metric"],
        "actions": ["scale_up"],
        "instance": instance,
        "envs": {"step": form.cleaned_data["units"]},
    }
    alarm_client.new(data, token)


def save_scale_down(form, instance, token):
    form_data = form.cleaned_data
    data = {
        "name": "scale_down_{}".format(instance),
        "expression": "%s %s %s" % (metrics["cpu"], form_data["operator"], form_data["value"]),
        "enabled": True,
        "wait": form.cleaned_data["wait"],
        "datasource": form.cleaned_data["metric"],
        "actions": ["scale_down"],
        "instance": instance,
        "envs": {"step": form.cleaned_data["units"]},
    }
    alarm_client.new(data, token)


def new(request, instance):
    token = request.GET.get("TSURU_TOKEN")

    scale_up_form = forms.ScaleForm(request.POST or None, prefix="scale_up")
    scale_down_form = forms.ScaleForm(request.POST or None, prefix="scale_down")
    config_form = forms.ConfigForm(request.POST or None)

    if scale_up_form.is_valid() and scale_down_form.is_valid() and config_form.is_valid():
        save_scale_up(scale_up_form, instance, token)
        save_scale_down(scale_down_form, instance, token)
        enable_alarm(config_form, instance, token)
        disable_alarm(config_form, instance, token)
        messages.success(request, u"Auto scale saved.")
        url = "{}?TSURU_TOKEN={}".format(reverse("instance-list"), token)
        return redirect(url)

    context = {
        "scale_up_form": scale_up_form,
        "scale_down_form": scale_down_form,
        "config_form": config_form,
    }

    return render(request, "wizard/index.html", context)
