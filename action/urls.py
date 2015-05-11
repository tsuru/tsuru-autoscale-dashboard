from django.conf.urls import url


urlpatterns = [
    url(r'^new/$', 'action.views.new', name='action-new'),
    url(r'^(?P<name>[\w\s-]+)/$', 'action.views.remove', name='action-remove'),
    url(r'^$', 'action.views.list', name='action-list'),
]
