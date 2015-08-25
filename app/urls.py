from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<app>[\w-]+)/$', "app.views.index", name='app-info'),
]
