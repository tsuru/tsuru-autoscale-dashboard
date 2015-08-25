from django.shortcuts import render


def index(request, app):
    return render(request, "app/index.html")
