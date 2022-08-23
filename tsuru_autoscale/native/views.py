import json

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import FormView, View
from tsuru_dashboard.apps.views import AppMixin
import requests

from tsuru_autoscale.wizard import client as wclient
from tsuru_autoscale.native import forms


class NativeAutoscale(AppMixin, FormView):
    template_name = "native/index.html"
    form_class = forms.ScaleForm

    def get_form(self):
        token = self.request.session.get('tsuru_token').split(" ")[-1]
        app_name = self.kwargs.get('app_name')
        form = forms.ScaleForm(self.request.POST or None)
        p_list = wclient.process_list(app_name, token)
        form.fields['process'].choices = p_list
        return form

    def get_context_data(self, *args, **kwargs):
        return super(NativeAutoscale, self).get_context_data(*self.args, **self.kwargs)

    def form_valid(self, form):
        token = self.request.session.get('tsuru_token').split(" ")[-1]
        app_name = self.kwargs.get('app_name')
        target_cpu = form.cleaned_data["target_cpu"]
        data = {
            "process": form.cleaned_data["process"],
            "minUnits": form.cleaned_data["min_units"],
            "maxUnits": form.cleaned_data["max_units"],
            "averageCPU": target_cpu,
        }

        try:
            add_autoscale(app_name, data, token)
        except Exception as e:
            messages.error(self.request, e)
            return self.form_invalid(form)
        else:
            messages.success(self.request, u"Auto scale saved.")
            url = reverse("autoscale-app-info", args=[app_name])
            return redirect(url)


class NativeAutoscaleRemove(AppMixin, View):
    def get(self, request, app_name, process):
        token = request.session.get('tsuru_token').split(" ")[-1]

        try:
            remove_autoscale(app_name, process, token)
        except Exception as e:
            messages.error(request, e)
        else:
            messages.success(request, u"Auto scale saved.")

        url = reverse("autoscale-app-info", args=[app_name])
        return redirect(url)


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
