from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'datasource.views.list'),
    url(r'^new/$', 'datasource.views.new'),
]
