from django.db import models
from django.utils.translation import ugettext_lazy as _


class News(models.Model):
    created = models.DateTimeField(_('Создание'), auto_now_add=True)
    title = models.CharField(_('Заголовок'), max_length=100, blank=False, null=False, default='', unique=True)
    slug = models.CharField(_('Ссылка'), max_length=100, blank=False, null=False, default='', unique=True)
    text = models.TextField(_('Текст новости'), max_length=5000, null=False, blank=False)
    is_public = models.BooleanField(_('Публиковать'), default=False)

    class Meta:
        verbose_name = _('новость')
        verbose_name_plural = _('новости')
        ordering = ('-pk',)