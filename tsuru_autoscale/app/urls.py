from django.conf.urls import url


urlpatterns = [
    url(r'^apps/(?P<app>[\w-]+)/autoscale/$', "tsuru_autoscale.app.views.index", name='app-info'),
]
