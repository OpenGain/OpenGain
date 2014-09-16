from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'default_set.dialogs.views.index', name='dialogs_index'),
                       url(r'^(?P<pk>\d+)/$', 'default_set.dialogs.views.detail', name='dialogs_detail'),

)
