from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'alarm.views.list'),
]
