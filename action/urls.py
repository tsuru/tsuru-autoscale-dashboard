from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'action.views.list'),
]
