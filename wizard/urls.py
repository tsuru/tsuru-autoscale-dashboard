from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<instance>[\w-]+)/$', 'wizard.views.new', name='wizard-new'),
    url(r'^(?P<instance>[\w-]+)/remove/$', 'wizard.views.remove', name='wizard-remove'),
    url(r'^$', 'wizard.views.new', name='wizard-new'),
]
