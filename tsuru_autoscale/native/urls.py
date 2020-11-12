from django.conf.urls import url

from tsuru_autoscale.native import views


urlpatterns = [
    url(r'^(?P<process>[\w-]+)/remove/$', views.remove, name='native-remove'),
    url(r'^$', views.new, name='native-new'),
]
