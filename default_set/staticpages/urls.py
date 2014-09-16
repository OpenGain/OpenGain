from django.conf.urls import patterns

urlpatterns = patterns('default_set.staticpages.views',
                       (r'^(?P<url>.*)$', 'staticpage'),
)
