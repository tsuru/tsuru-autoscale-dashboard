from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'datasource.views.list', name='datasource-list'),
    url(r'^new/$', 'datasource.views.new', name='datasource-new'),
    url(r'^(?P<name>[\w\s-]+)/remove/$', 'datasource.views.remove', name='datasource-remove'),
    url(r'^(?P<name>[\w\s-]+)/$', 'datasource.views.get', name='datasource-get'),
]
