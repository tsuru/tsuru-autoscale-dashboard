from django.conf.urls import include, url

from tsuru_autoscale.instance import views


urlpatterns = [
    url(r'^instance/$', views.list, name='instance-list'),
    url(r'^datasource/', include('tsuru_autoscale.datasource.urls')),
    url(r'^alarm/', include('tsuru_autoscale.alarm.urls')),
    url(r'^action/', include('tsuru_autoscale.action.urls')),
    url(r'^instance/', include('tsuru_autoscale.instance.urls')),
    url(r'^wizard/', include('tsuru_autoscale.wizard.urls')),
    url(r'^', include('tsuru_autoscale.app.urls')),
]
