from django.db import models
from django.utils import timezone
from default_set.models import *
from main import discovers
from django.utils.translation import ugettext_lazy as _
from decimal import *

class Deposit(models.Model):
    created = models.DateTimeField(_('Создание'), auto_now=False, auto_now_add=True, null=False, blank=False,
                                   default=timezone.now)
    last_update = models.DateTimeField(_('Изменение'), auto_now=True, auto_now_add=True, null=False, blank=False,
                                       default=timezone.now)
    user = models.ForeignKey('default_set.UserProfile', related_name='deposits', verbose_name=_('Пользователь'), null=True,
                             blank=False, db_index=True)
    ps = models.CharField(_('Платежка'), max_length=20, choices=discovers.PAYMENT_SYSTEMS_TUPLE, null=True, blank=False,
                          db_index=True)
    amount = models.DecimalField(_('Сумма'), max_digits=8, decimal_places=2, default=0, null=False, blank=False)
    is_ended = models.BooleanField(_('Завершено'), default=False, db_index=True)
    plan = models.ForeignKey('default_set.Plan', related_name='plan_deposits', verbose_name=_('План'), null=False,
                             blank=False, db_index=True)


    class Meta:
        ordering = ('-id',)
        verbose_name = _('Депозит')
        verbose_name_plural = _('Депозиты')


    def get_accrued_amount(self):
        return self.deposit_transactions.filter(transaction_type=TRANSACTION_ACCRUAL).aggregate(Sum('amount'))['amount__sum'] or 0

    def get_next_accrual(self):
        deltas = {
            1: timezone.timedelta(hours=1),
            2: timezone.timedelta(days=1),
            3: timezone.timedelta(weeks=1),
            4: timezone.timedelta(days=30),
        }
        next_amount = self.amount / Decimal('100.00') * self.plan.percent
        next_datetime = self.last_update + deltas[self.plan.period]
        return dict(datetime=next_datetime, amount=next_amount)

    def __str__(self):
        return '{}/{}'.format(self.plan.title, self.amount)
