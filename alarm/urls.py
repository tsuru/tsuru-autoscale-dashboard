from django.conf.urls import url


urlpatterns = [
    url(r'^new/$', 'alarm.views.new'),
    url(r'^$', 'alarm.views.list'),
]
