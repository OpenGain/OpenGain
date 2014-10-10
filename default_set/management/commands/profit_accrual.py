import importlib
from django.core.management.base import BaseCommand, CommandError
from default_set.deposits.models import Deposit
from default_set.models import *
from django.utils import timezone
from default_set.transactions import UserTransaction
from main.discovers import PAYMENT_SYSTEMS
from decimal import *
from django.conf import settings

deltas = {
    PLAN_PERIOD_HOUR: timezone.timedelta(hours=1),
    PLAN_PERIOD_DAY: timezone.timedelta(days=1),
    PLAN_PERIOD_WEEK: timezone.timedelta(weeks=1),
    PLAN_PERIOD_MONTH: timezone.timedelta(days=30),
}


def accrual_balances():
    users = UserProfile.objects.all()
    for user in users:

        for ps in user.get_ps_instances():
            plan = Plan.objects.get_plan_by_amount(ps.balance)

            if plan:
                delta = timezone.now() - deltas[plan.period]
                accrual_transactions = user.transactions.filter(ps=ps.get_name,
                                                                transaction_type=TRANSACTION_ACCRUAL,
                                                                is_ended=True, created__gte=delta)
                if not accrual_transactions:
                    utr = UserTransaction()
                    utr.do_transaction_accrual(user, ps.get_name, ps.balance / Decimal(100) * plan.percent)

def accrual_deposits():
    deposits = Deposit.objects.filter(is_ended=False)
    for deposit in deposits:
        plan = deposit.plan
        time_elapsed = timezone.now()-deposit.last_update
        delta = deltas[plan.period]
        if time_elapsed >= delta:
            deposit.last_update = timezone.now()
            deposit.save()
            utr = UserTransaction()
            utr.do_transaction_accrual(deposit.user, deposit.ps, deposit.amount / Decimal(100) * plan.percent, deposit=deposit)

        if int((timezone.now()-deposit.created).total_seconds()/3600) >= plan.end_period:
            deposit.is_ended = True
            deposit.save()

            if plan.deposit_return:
                utr = UserTransaction()
                utr.do_deposit_return(deposit)


class Command(BaseCommand):
    def handle(self, *args, **options):
        if settings.USE_DEPOSITS:
            accrual_deposits()
        else:
            accrual_balances()




