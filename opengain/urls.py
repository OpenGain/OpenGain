from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from main import opengain_admin
from django.conf import settings

urlpatterns = patterns('',
                       url(r'^$', 'main.views.index', name='index'),
                       url(r'^user/', include('default_set.urls')),
                       url(r'^reviews/', include('default_set.reviews.urls')),
                       url(r'^news/', include('default_set.news.urls')),
                       (r'^pages/', include('default_set.staticpages.urls')),
                       (r'^i18n/', include('django.conf.urls.i18n')),

                       url(r'^' + settings.ADMIN_URL + '/', include(opengain_admin.urls)),
                       url(r'^' + settings.TRANSLATION_URL + '/', include('rosetta.urls')),
                       url(r'^(?P<b64>[0-9A-Za-z_\-]+)/$', 'default_set.views.sponsor_redirect',
                           name='sponsor_redirect'),
)
