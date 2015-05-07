from django.conf.urls import url


urlpatterns = [
    url(r'^new/$', 'alarm.views.new', name='alarm-new'),
    url(r'^$', 'alarm.views.list', name='alarm-list'),
]
