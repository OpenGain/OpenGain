from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import get_script_prefix
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import iri_to_uri


class StaticPage(models.Model):
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('заголовок'), max_length=200)
    content = models.TextField(_('содержание'), blank=True)
    template_name = models.CharField(_('имя шаблона'), max_length=70, blank=True,
                                     help_text=_(
                                         "Пример: 'staticpages/contact_page.html'. Если не предусмотрен, система будет использовать 'staticpages/default.html'."))

    class Meta:
        verbose_name = _('статическая страница')
        verbose_name_plural = _('статические страницы')
        ordering = ('url',)

    def __str__(self):
        return "%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        # Handle script prefix manually because we bypass reverse()
        return iri_to_uri(get_script_prefix().rstrip('/') + self.url)
