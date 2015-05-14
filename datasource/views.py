from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from datasource.forms import DataSourceForm
from datasource import client


def new(request):
    form = DataSourceForm(request.POST or None)

    if form.is_valid():
        token = request.GET.get("TSURU_TOKEN")
        client.new(form.cleaned_data, token)
        messages.success(request, u"Data source saved.")
        url = "{}?TSURU_TOKEN={}".format(reverse('datasource-list'), token)
        return redirect(url)

    context = {"form": form}
    return render(request, "datasource/new.html", context)


def list(request):
    token = request.GET.get("TSURU_TOKEN")
    datasources = client.list(token).json()
    context = {
        "list": datasources,
    }
    return render(request, "datasource/list.html", context)


def remove(request, name):
    token = request.GET.get("TSURU_TOKEN")
    client.remove(name, token)
    messages.success(request, u"Data source  {} remove.".format(name))
    url = "{}?TSURU_TOKEN={}".format(reverse('datasource-list'), token)
    return redirect(url)


def get(request, name):
    token = request.GET.get("TSURU_TOKEN")
    datasource = client.get(name, token).json()
    context = {
        "item": datasource,
    }
    return render(request, "datasource/get.html", context)
