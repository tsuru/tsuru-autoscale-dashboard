from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'alarm.views.list', name='alarm-list'),
    url(r'^new/$', 'alarm.views.new', name='alarm-new'),
    url(r'^(?P<name>[\w\s-]+)/$', 'alarm.views.remove', name='alarm-remove'),
]
