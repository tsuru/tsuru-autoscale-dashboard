from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'tsuru_autoscale.datasource.views.list', name='datasource-list'),
    url(r'^new/$', 'tsuru_autoscale.datasource.views.new', name='datasource-new'),
    url(r'^(?P<name>[\w\s-]+)/remove/$', 'tsuru_autoscale.datasource.views.remove', name='datasource-remove'),
    url(r'^(?P<name>[\w\s-]+)/$', 'tsuru_autoscale.datasource.views.get', name='datasource-get'),
]
