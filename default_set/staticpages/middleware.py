from .views import staticpage
from django.http import Http404
from django.conf import settings


class StaticpageFallbackMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response
        try:
            return staticpage(request, request.path_info)
        except Http404:
            return response
        except Exception:
            if settings.DEBUG:
                raise
            return response
