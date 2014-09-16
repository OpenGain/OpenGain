from django.contrib.auth import logout
from django.conf import settings


class DeactivateUserMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            if not request.user.is_active:
                logout(request)


class ChangeUserLanguage(object):
    def process_request(self, request):
        if request.LANGUAGE_CODE != request.session.get('user_lang', None) and request.user.is_authenticated():
            request.session['user_lang'] = request.LANGUAGE_CODE
            user = request.user
            user.lang = request.LANGUAGE_CODE
            user.save()

