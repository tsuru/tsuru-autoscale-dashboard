from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from datasource.forms import DataSourceForm
from datasource import client


def new(request):
    form = DataSourceForm(request.POST or None)

    if form.is_valid():
        client.new(form.cleaned_data)
        messages.success(request, u"Data source saved.")
        return redirect(reverse('datasource-list'))

    context = {"form": form}
    return render(request, "datasource/new.html", context)


def list(request):
    datasources = client.list().json()
    context = {
        "list": datasources,
    }
    return render(request, "datasource/list.html", context)
