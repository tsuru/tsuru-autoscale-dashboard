import json

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from tsuru_dashboard import engine
import requests

from tsuru_autoscale.wizard import client as wclient
from tsuru_autoscale.native import forms


def add_autoscale(app, data, token):
    url = "{}/apps/{}/units/autoscale".format(wclient.tsuru_host(), app)
    headers = {
        "Authorization": wclient.clean_token(token),
        "Content-Type": "application/json",
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code != 200:
        raise Exception(
            'Invalid response {}: {}'.format(response.status_code, response.text),
        )


def remove_autoscale(app, process, token):
    url = "{}/apps/{}/units/autoscale?process={}".format(wclient.tsuru_host(), app, process)
    headers = {
        "Authorization": wclient.clean_token(token),
        "Content-Type": "application/json",
    }
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        raise Exception('invalid response {}: {}'.format(response.status_code, response.text))


def new(request, app):
    token = request.session.get('tsuru_token').split(" ")[-1]

    form = forms.ScaleForm(request.POST or None)
    p_list = wclient.process_list(app, token)
    form.fields['process'].choices = p_list

    if form.is_valid():
        cpuMilli = form.cleaned_data["target_cpu"] * 10
        data = {
            "process": form.cleaned_data["process"],
            "minUnits": form.cleaned_data["min_units"],
            "maxUnits": form.cleaned_data["max_units"],
            "averageCPU": '{}m'.format(cpuMilli),
        }
        try:
            add_autoscale(app, data, token)
        except Exception as e:
            messages.error(request, e)
        else:
            messages.success(request, u"Auto scale saved.")
            url = reverse("autoscale-app-info", args=[app])
            return redirect(url)

    app_info = wclient.app_info(app, token)
    context = {
        "form": form,
        "app": app_info,
        "tabs": engine.get('app').tabs,
    }
    return render(request, "native/index.html", context)


def remove(request, app, process):
    token = request.session.get('tsuru_token').split(" ")[-1]

    try:
        remove_autoscale(app, process, token)
    except Exception as e:
        messages.error(request, e)
    else:
        messages.success(request, u"Auto scale saved.")

    url = reverse("autoscale-app-info", args=[app])
    return redirect(url)
