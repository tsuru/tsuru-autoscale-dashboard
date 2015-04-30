from django.shortcuts import render

from datasource.forms import DataSourceForm


def new(request):
    context = {
        "form": DataSourceForm()
    }
    return render(request, "datasource/new.html", context)
