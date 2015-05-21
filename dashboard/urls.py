from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', include('instance.urls')),
    url(r'^datasource/', include('datasource.urls')),
    url(r'^alarm/', include('alarm.urls')),
    url(r'^action/', include('action.urls')),
]
