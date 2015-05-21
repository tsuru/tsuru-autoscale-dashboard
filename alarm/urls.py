from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'alarm.views.list', name='alarm-list'),
    url(r'^new/$', 'alarm.views.new', name='alarm-new'),
    url(r'^(?P<name>[\w\s-]+)/remove/$', 'alarm.views.remove', name='alarm-remove'),
    url(r'^(?P<alarm_name>[\w\s-]+)/event/$', 'event.views.list', name='event-list'),
    url(r'^(?P<name>[\w\s-]+)/$', 'alarm.views.get', name='alarm-get'),
]
