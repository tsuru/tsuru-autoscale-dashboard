from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<name>[\w-]+)/$', 'instance.views.get', name='instance-get'),
]
