from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TicketsConfig(AppConfig):
    name = 'default_set.tickets'
    verbose_name = _('Тикеты')
