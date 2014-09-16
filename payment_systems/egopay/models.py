from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
import re
from django.conf import settings
from . import NAME, TITLE
from django.utils.translation import ugettext_lazy as _


class PSForUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('Пользователь'), null=False, blank=False,
                                related_name=NAME)
    wallet = models.CharField(verbose_name=_('Кошелек EgoPay'), default=None, null=True, blank=True, max_length=45,
                              validators=[validate_email, ], db_index=True)
    balance = models.DecimalField(verbose_name=_('Баланс'), default=0, null=False, blank=False, max_digits=8,
                                  decimal_places=2)

    class Meta:
        verbose_name = 'egopay'
        verbose_name_plural = 'egopay'

    def __str__(self):
        return '{} = ${}'.format(self.wallet, self.balance)

    @property
    def get_name(self):
        return NAME

    @property
    def get_title(self):
        return TITLE
