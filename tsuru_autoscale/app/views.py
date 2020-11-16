import os

from django.views.generic import TemplateView

from tsuru_autoscale.instance import client
from tsuru_autoscale.wizard import client as wclient
from tsuru_dashboard.apps.views import AppMixin


class AutoscaleApp(AppMixin, TemplateView):
    template_name = 'app/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AutoscaleApp, self).get_context_data(*args, **kwargs)

        token = self.request.session.get('tsuru_token').split(" ")[-1]
        instances = client.list(token).json() or []

        app = context.get('app', {})
        pool_name = app.get('pool')
        pool_info = wclient.pool_info(pool_name, token) if pool_name else None

        provisioner = pool_info.get('provisioner') if pool_info else None

        native_disable = os.environ.get("AUTOSCALE_NATIVE_DISABLE") in ["True", "1", "true"]
        supports_native = provisioner == "kubernetes" and not native_disable

        instance = None
        auto_scale = None
        events = None
        legacy = self.request.GET.get('legacy')

        for inst in instances:
            if app.get('name') in inst.get('Apps', []):
                instance = inst

                response = wclient.get(instance["Name"], token)
                if response.status_code == 200:
                    auto_scale = response.json()
                    events = wclient.events(instance["Name"], token).json()

        context.update({
            "instance": instance,
            "auto_scale": auto_scale,
            "events": events,
            "supports_native": supports_native,
            "is_legacy": legacy == "1" or legacy == "true" or legacy == "True" or not supports_native,
        })
        return context
