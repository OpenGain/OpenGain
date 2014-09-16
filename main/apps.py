from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ApplicationConfig(AppConfig):
    name = 'main'
    verbose_name = _("Основное")

