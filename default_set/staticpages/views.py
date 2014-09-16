from django.conf import settings
from .models import StaticPage
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect

DEFAULT_TEMPLATE = 'staticpages/default.html'


def staticpage(request, url):
    if not url.startswith('/'):
        url = '/' + url
    try:
        f = get_object_or_404(StaticPage,
                              url=url)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            f = get_object_or_404(StaticPage,
                                  url=url)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    return render_staticpages(request, f)


@csrf_protect
def render_staticpages(request, f):
    if f.template_name:
        t = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)

    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)

    c = RequestContext(request, {
        'staticpage': f,
    })
    response = HttpResponse(t.render(c))
    return response
