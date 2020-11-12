from django.conf.urls import url, include

from tsuru_autoscale.app import views

urlpatterns = [
    url(r'^apps/(?P<app>[\w-]+)/autoscale/$', views.index, name='autoscale-app-info'),
    url(r'^apps/(?P<app>[\w-]+)/autoscale/native/', include('tsuru_autoscale.native.urls')),
]
