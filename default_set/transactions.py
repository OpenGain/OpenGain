from django.db.models import F
from default_set.deposits.models import Deposit
from .models import *
from django.db import transaction
from decimal import *
from django.utils.translation import ugettext_lazy as _


def calculate_admin_salary(amount):
    return amount / Decimal(100) * settings.WITHDRAW_COMISSION_PERCENT


def calculate_withdraw_amount(amount):
    return amount - calculate_admin_salary(amount)


class InsufficientBalance(Exception):
    def __str__(self):
        return _('Недостаточно средств')


class UserTransaction(object):
    user = None
    ps = None
    amount = 0
    transaction_type = None
    other_user = None
    error_code = 0
    balance_before = 0
    balance_after = 0
    ps_instance = None
    ps_class = None

    # @transaction.atomic
    # def lock_user(self):
    # return UserProfile.objects.select_for_update().get(pk=self.user.pk)

    @transaction.atomic
    def lock_ps_instance(self):
        return self.user.get_ps_class(self.ps).objects.select_for_update().get(pk=self.ps_instance.pk)

    def _do_transaction(self, change_balance=True):
        self.balance_before = self.ps_instance.balance

        if change_balance:
            locked_ps_instance = self.lock_ps_instance()

            if locked_ps_instance.balance + self.amount < 0:
                raise InsufficientBalance
            locked_ps_instance.balance = F('balance') + self.amount
            locked_ps_instance.save()

        self.ps_class = self.user.get_ps_class(self.ps)
        self.ps_instance = self.ps_class.objects.get(pk=self.ps_instance.pk)

        if change_balance:
            self.balance_after = self.ps_instance.balance
        else:
            self.balance_after = self.balance_before

    @transaction.atomic
    def do_transaction_deposit(self, user, tr, batch):
        self.ps_instance = user.get_ps_instance(tr.ps)
        self.user = user
        self.ps = tr.ps
        self.amount = tr.amount

        self._do_transaction(change_balance=False)

        deposit = None

        if settings.USE_DEPOSITS:
            plan = Plan.objects.get_plan_by_amount(self.amount)
            if plan:
                deposit = Deposit.objects.create(user=self.user, ps=self.ps, amount=self.amount, plan=plan)


        self.transaction = Transaction.objects.select_for_update().get(pk=tr.pk)

        self.transaction.balance_before = self.balance_before
        self.transaction.balance_after = self.balance_after
        self.transaction.batch = batch
        self.transaction.is_ended = True
        self.transaction.save()

        if settings.USE_DEPOSITS:
            deposit.transactions.add(self.transaction)


        if settings.REFERRAL_COMISSION_POINT == 'deposit':
            sponsors = user.get_sponsors_and_percents()
            for sponsor in sponsors:
                self.do_transaction_referral(sponsor[0], self.ps, self.amount / Decimal(100) * sponsor[1], other_user=user)


    def do_transaction_withdraw(self, user, ps, amount):
        self.ps_instance = user.get_ps_instance(ps)
        self.user = user
        self.ps = ps
        self.amount = -amount

        self._do_transaction()
        amount_for_withdraw = amount - calculate_admin_salary(amount)
        self.transaction = self.user.transactions.create(ps=self.ps, amount=-amount_for_withdraw,
                                                         transaction_type=TRANSACTION_WITHDRAW,
                                                         balance_before=self.balance_before,
                                                         balance_after=self.balance_after)



    def do_transaction_transfer(self, user, ps, amount, other_user):
        self.ps_instance = user.get_ps_instance(ps)
        self.user = user
        self.ps = ps
        self.amount = -amount

        self._do_transaction()
        self.transaction = self.user.transactions.create(ps=self.ps, amount=self.amount,
                                                         transaction_type=TRANSACTION_TRANSFER_OUTGOING,
                                                         balance_before=self.balance_before,
                                                         balance_after=self.balance_after,
                                                         is_ended=True)

        self.ps_instance = other_user.get_ps_instance(ps)
        self.user = other_user
        self.amount = amount

        self._do_transaction()
        self.transaction = self.user.transactions.create(ps=self.ps, amount=self.amount,
                                                         transaction_type=TRANSACTION_TRANSFER_INCOMING,
                                                         balance_before=self.balance_before,
                                                         balance_after=self.balance_after,
                                                         is_ended=True)


    def do_transaction_referral(self, user, ps, amount, other_user):
        self.ps_instance = user.get_ps_instance(ps)
        self.user = user
        self.ps = ps
        self.amount = amount

        self._do_transaction()
        self.transaction = self.user.transactions.create(ps=self.ps, amount=self.amount,
                                                         transaction_type=TRANSACTION_REFERRAL,
                                                         balance_before=self.balance_before,
                                                         balance_after=self.balance_after, other_user=other_user,
                                                         is_ended=True)
        if user.is_alerts_comission:
            self.user.email_user(_('Реферальная комиссия'), 'mail/comission.html', dict(
                ps=self.transaction.get_ps_display(), amount=amount, balance=self.balance_after, referral=other_user
            ))


    def do_transaction_accrual(self, user, ps, amount, deposit=None):
        self.ps_instance = user.get_ps_instance(ps)
        self.user = user
        self.ps = ps
        self.amount = amount

        self._do_transaction()
        self.transaction = self.user.transactions.create(ps=self.ps, amount=self.amount,
                                                         transaction_type=TRANSACTION_ACCRUAL,
                                                         balance_before=self.balance_before,
                                                         balance_after=self.balance_after, is_ended=True)
        if deposit:
            deposit.transactions.add(self.transaction)

        if settings.REFERRAL_COMISSION_POINT == 'accrual':
            sponsors = user.get_sponsors_and_percents()
            for sponsor in sponsors:
                self.do_transaction_referral(sponsor[0], ps, amount / Decimal(100) * sponsor[1], other_user=user)

    def do_deposit_return(self, deposit):
        self.ps_instance = deposit.user.get_ps_instance(deposit.ps)
        self.user = deposit.user
        self.ps = deposit.ps
        self.amount = deposit.amount

        self._do_transaction()
        self.transaction = self.user.transactions.create(ps=self.ps, amount=self.amount,
                                                         transaction_type=TRANSACTION_DEPOSIT_RETURN,
                                                         balance_before=self.balance_before,
                                                         balance_after=self.balance_after, is_ended=True)
        deposit.transactions.add(self.transaction)

