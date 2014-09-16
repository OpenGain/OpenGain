from django.db import models
from django.conf import settings
from django.db.models.query import Q
from django.utils.translation import ugettext_lazy as _


class Dialog(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('Участники диалога'),
                                   related_name='dialogs')

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Диалог')
        verbose_name_plural = _('Диалоги')

    def __str__(self):
        return ' vs '.join(user.username for user in self.users.all())

    def get_unreaded_count(self, user):
        return self.messages.filter(~Q(user=user), is_readed=False).count()

    def get_messages_count(self):
        return self.messages.count()

    def get_sender(self):
        return self.messages.first().user

    def get_receiver(self):
        return self.users.exclude(pk=self.get_sender().pk).get()


class DialogMessage(models.Model):
    dialog = models.ForeignKey(Dialog, verbose_name=_('Диалог'), related_name='messages', null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Пользователь'), related_name='dialog_messages',
                             null=True, blank=False, default=None)
    created = models.DateTimeField(_('Дата содания'), auto_now_add=True, auto_now=False)
    message = models.TextField(_('Сообщение'), max_length=500, null=False, blank=False)
    is_readed = models.BooleanField(_('Прочитано'), default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Сообщение в диалоге')
        verbose_name_plural = _('Сообщения в диалогах')
