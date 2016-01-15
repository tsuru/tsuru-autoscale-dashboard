from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'tsuru_autoscale.alarm.views.list', name='alarm-list'),
    url(r'^new/$', 'tsuru_autoscale.alarm.views.new', name='alarm-new'),
    url(r'^(?P<name>[\w\s-]+)/remove/$', 'tsuru_autoscale.alarm.views.remove', name='alarm-remove'),
    url(r'^(?P<alarm_name>[\w\s-]+)/event/$', 'tsuru_autoscale.event.views.list', name='event-list'),
    url(r'^(?P<name>[\w\s-]+)/$', 'tsuru_autoscale.alarm.views.get', name='alarm-get'),
]
