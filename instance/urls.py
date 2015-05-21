from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'instance.views.list', name='instance-list'),
]
