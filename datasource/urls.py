from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'datasource.views.list', name='datasource-list'),
    url(r'^new/$', 'datasource.views.new', name='datasource-new'),
]
