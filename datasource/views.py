from django.shortcuts import render, redirect

from datasource.forms import DataSourceForm
from datasource import client


def new(request):
    form = DataSourceForm(request.POST or None)

    if form.is_valid():
        client.new(form.cleaned_data)
        return redirect('/datasource/')

    context = {"form": form}
    return render(request, "datasource/new.html", context)


def list(request):
    datasources = client.list()
    context = {
        "list": datasources,
    }
    return render(request, "datasource/list.html", context)
