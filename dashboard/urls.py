from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', 'instance.views.list', name='instance-list'),
    url(r'^datasource/', include('datasource.urls')),
    url(r'^alarm/', include('alarm.urls')),
    url(r'^action/', include('action.urls')),
    url(r'^instance/', include('instance.urls')),
]
