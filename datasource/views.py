from django.shortcuts import render

from datasource.forms import DataSourceForm
from datasource import client


def new(request):
    form = DataSourceForm(request.POST or {})
    if form.is_valid():
        pass
    context = {"form": form}
    return render(request, "datasource/new.html", context)


def list(request):
    datasources = client.list()
    context = {
        "list": datasources,
    }
    return render(request, "datasource/list.html", context)
