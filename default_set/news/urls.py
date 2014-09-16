from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'default_set.news.views.index', name='news_index'),
                       url(r'^(?P<slug>[\w-]+)/$', 'default_set.news.views.detail',
                           name='news_detail'),
)