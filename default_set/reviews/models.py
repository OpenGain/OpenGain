from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Review(models.Model):
    created = models.DateTimeField(_('Создание'), auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Пользователь'), null=False, blank=False,
                             related_name='reviews')
    review = models.TextField(_('Отзыв'), max_length=500, null=False, blank=False)
    admin_answer = models.TextField(_('Ответ админа'), max_length=500, null=True, blank=True)
    is_public = models.BooleanField(_('Публиковать'), default=False)

    class Meta:
        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')
        ordering = ('-pk',)
