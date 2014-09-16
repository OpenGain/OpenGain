from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy as _

default_app_config = 'main.apps.ApplicationConfig'

class OpenGainAdmin(AdminSite):
    site_header = _('Админка OpenGain Engine')
    site_title = _('Админка OpenGain Engine')
    index_title = _('Администрирование проекта')

opengain_admin = OpenGainAdmin()