from django.shortcuts import render

from datasource.forms import DataSourceForm


def new(request):
    form = DataSourceForm(request.POST or {})
    if form.is_valid():
        pass
    context = {"form": form}
    return render(request, "datasource/new.html", context)
