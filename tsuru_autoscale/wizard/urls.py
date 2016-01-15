from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<instance>[\w-]+)/$', 'tsuru_autoscale.wizard.views.new', name='wizard-new'),
    url(r'^(?P<instance>[\w-]+)/remove/$', 'tsuru_autoscale.wizard.views.remove', name='wizard-remove'),
    url(r'^$', 'tsuru_autoscale.wizard.views.new', name='wizard-new'),
]
