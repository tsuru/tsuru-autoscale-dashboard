from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from tsuru_autoscale.wizard import forms
from tsuru_autoscale.wizard import client
from tsuru_autoscale.datasource import client as dclient

import requests
import urllib


def get_or_create_tsuru_instance(instance_name, token):
    token = urllib.unquote(token)
    token = "bearer {}".format(token)
    url = "{}/services/autoscale/instances/{}".format(client.tsuru_host(), instance_name)
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return

    app = client.app_info(instance_name, token)
    url = "{}/services/autoscale/instances".format(client.tsuru_host(), instance_name)
    headers = {"Authorization": token, "Content-Type": "application/x-www-form-urlencoded"}
    data = {"service_name": "autoscale", "name": instance_name, "owner": app["teamowner"]}
    response = requests.post(url, headers=headers, data=data)

    url = "{}/services/{}/instances/{}/{}".format(client.tsuru_host(), "autoscale", instance_name, instance_name)
    headers = {"Authorization": token}
    response = requests.put(url, headers=headers, data={"noRestart": "true"})


def new(request, instance=None):
    token = request.session.get('tsuru_token').split(" ")[-1]

    dlist = [(d["Name"], d["Name"]) for d in dclient.list(token).json()]

    scale_up_form = forms.ScaleForm(30, request.POST or None, prefix="scale_up", initial={"operator": ">"})
    scale_up_form.fields['metric'].choices = dlist

    scale_down_form = forms.ScaleForm(60, request.POST or None, prefix="scale_down", initial={"operator": "<"})
    scale_down_form.fields['metric'].choices = dlist

    config_form = forms.ConfigForm(request.POST or None)

    p_list = client.process_list(instance, token)
    config_form.fields['process'].choices = p_list

    if scale_up_form.is_valid() and scale_down_form.is_valid() and config_form.is_valid():
        get_or_create_tsuru_instance(instance, token)
        config_data = {
            "name": instance,
            "minUnits": config_form.cleaned_data["min"],
            "scaleUp": scale_up_form.cleaned_data,
            "scaleDown": scale_down_form.cleaned_data,
            "process": config_form.cleaned_data["process"],
        }
        client.new(config_data, token)
        messages.success(request, u"Auto scale saved.")
        url = reverse("autoscale-app-info", args=[instance])
        return redirect(url)

    token = urllib.quote(token)
    context = {
        "scale_up_form": scale_up_form,
        "scale_down_form": scale_down_form,
        "config_form": config_form,
        "token": token,
    }

    return render(request, "wizard/index.html", context)


def remove(request, instance):
    token = request.session.get('tsuru_token').split(" ")[-1]
    client.remove(instance, token)
    messages.success(request, u"Auto scale {} removed.".format(instance))
    url = reverse("autoscale-app-info", args=[instance])
    return redirect(url)


def enable(request, instance):
    token = request.session.get('tsuru_token').split(" ")[-1]
    client.enable(instance, token)
    messages.success(request, u"Auto scale {} enabled.".format(instance))
    url = reverse("autoscale-app-info", args=[instance])
    return redirect(url)


def disable(request, instance):
    token = request.session.get('tsuru_token').split(" ")[-1]
    client.disable(instance, token)
    messages.success(request, u"Auto scale {} disabled.".format(instance))
    url = reverse("autoscale-app-info", args=[instance])
    return redirect(url)
