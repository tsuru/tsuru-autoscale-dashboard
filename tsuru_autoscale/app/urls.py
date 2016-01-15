from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<app>[\w-]+)/$', "tsuru_autoscale.app.views.index", name='app-info'),
]
