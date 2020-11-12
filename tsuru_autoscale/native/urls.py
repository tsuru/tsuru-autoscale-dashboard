from django.conf.urls import url

from tsuru_autoscale.native import views


urlpatterns = [
    url(r'^(?P<process>[\w-]+)/remove/$', views.NativeAutoscaleRemove.as_view(), name='native-remove'),
    url(r'^$', views.NativeAutoscale.as_view(), name='native-new'),
]
