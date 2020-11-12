from django.conf.urls import url, include

from tsuru_autoscale.app import views

urlpatterns = [
    url(r'^apps/(?P<app_name>[\w-]+)/autoscale/$', views.AutoscaleApp.as_view(), name='autoscale-app-info'),
    url(r'^apps/(?P<app_name>[\w-]+)/autoscale/native/', include('tsuru_autoscale.native.urls')),
]
