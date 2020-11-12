from django.shortcuts import render

from tsuru_autoscale.instance import client
from tsuru_autoscale.wizard import client as wclient
from tsuru_dashboard import engine


def index(request, app):
    token = request.session.get('tsuru_token').split(" ")[-1]
    instances = client.list(token).json() or []

    app_info = wclient.app_info(app, token)
    pool_info = wclient.pool_info(app_info.get('pool'), token)

    provisioner = pool_info.get('provisioner') if pool_info else None
    supports_native = provisioner == "kubernetes"

    instance = None
    auto_scale = None
    events = None
    legacy = request.GET.get('legacy')

    for inst in instances:
        if app in inst.get('Apps', []):
            instance = inst

            response = wclient.get(instance["Name"], token)
            if response.status_code == 200:
                auto_scale = response.json()
                events = wclient.events(instance["Name"], token).json()
    context = {
        "instance": instance,
        "auto_scale": auto_scale,
        "events": events,
        "app": app_info,
        "tabs": engine.get('app').tabs,
        "supports_native": supports_native,
        "is_legacy": legacy == "1" or legacy == "true" or legacy == "True" or not supports_native,
    }
    return render(request, "app/index.html", context)
