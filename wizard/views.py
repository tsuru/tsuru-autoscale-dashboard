from django.shortcuts import render

from wizard import forms


def index(request):
    context = {
        "scale_up_form": forms.ScaleForm(),
        "scale_down_form": forms.ScaleForm(),
        "config_form": forms.ConfigForm(),
    }

    return render(request, "wizard/index.html", context)
