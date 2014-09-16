from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class StaticPagesConfig(AppConfig):
    name = 'default_set.staticpages'
    verbose_name = _('Статические страницы')
