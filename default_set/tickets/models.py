from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Ticket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Пользователь'), related_name='tickets',
                             null=True, blank=False, default=None)
    created = models.DateTimeField(_('Дата создания'), auto_now_add=True, auto_now=False)
    subject = models.CharField(_('Тема'), max_length=100, null=False, blank=False)
    is_closed = models.BooleanField(_('Закрыт'), default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('тикет')
        verbose_name_plural = _('тикеты')

    def __str__(self):
        return _("{}#тема:{}").format(self.user, self.subject)

    def get_unread_message_count(self):
        return self.messages.filter(is_readed=False).count()


class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, verbose_name=_('Тикет'), related_name='messages', null=False, blank=False)
    created = models.DateTimeField(_('Дата содания'), auto_now_add=True, auto_now=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Пользователь'), related_name='tickets_messages',
                             null=True, blank=False, default=None)
    message = models.TextField(_('Сообщение'), max_length=500, null=False, blank=False)
    is_readed = models.BooleanField(_('Прочитан'), default=False)

    def __str__(self):
        return "{}".format(self.ticket)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('сообщение тикета')
        verbose_name_plural = _('сообщения тикетов')
