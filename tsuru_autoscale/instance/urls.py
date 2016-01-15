from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<name>[\w-]+)/$', 'tsuru_autoscale.instance.views.get', name='instance-get'),
]
