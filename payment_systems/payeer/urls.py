from django.conf.urls import patterns, url
from .views import *
from . import NAME


urlpatterns = patterns('',
                       url(r'^result/$', deposit_result, name='deposit_result_' + NAME),
)