from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'default_set.tickets.views.index', name='tickets_index'),
                       url(r'^create/$', 'default_set.tickets.views.create', name='tickets_create'),
                       url(r'^(?P<pk>\d+)/$', 'default_set.tickets.views.detail',
                           name='tickets_detail'),
                       url(r'^close/(?P<pk>\d+)/$', 'default_set.tickets.views.close',
                           name='tickets_close'),
)