from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ApplicationConfig(AppConfig):
    name = 'default_set.reviews'
    verbose_name = _("Отзывы")

