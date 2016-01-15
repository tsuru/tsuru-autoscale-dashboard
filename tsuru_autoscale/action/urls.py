from django.conf.urls import url


urlpatterns = [
    url(r'^new/$', 'tsuru_autoscale.action.views.new', name='action-new'),
    url(r'^(?P<name>[\w\s-]+)/remove/$', 'tsuru_autoscale.action.views.remove', name='action-remove'),
    url(r'^(?P<name>[\w\s-]+)/$', 'tsuru_autoscale.action.views.get', name='action-get'),
    url(r'^$', 'tsuru_autoscale.action.views.list', name='action-list'),
]
