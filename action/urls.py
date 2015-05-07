from django.conf.urls import url


urlpatterns = [
    url(r'^new/$', 'action.views.new'),
    url(r'^$', 'action.views.list'),
]
