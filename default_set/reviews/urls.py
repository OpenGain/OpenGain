from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'default_set.reviews.views.index', name='reviews_index'),
)
