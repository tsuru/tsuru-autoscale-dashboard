from django.conf.urls import include, url


urlpatterns = [
    url(r'^datasource/', include('datasource.urls')),
    url(r'^alarm/', include('alarm.urls')),
]
