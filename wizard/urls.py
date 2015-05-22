from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'wizard.views.index', name='wizard-index'),
]
