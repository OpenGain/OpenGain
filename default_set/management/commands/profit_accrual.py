import importlib
from django.core.management.base import BaseCommand, CommandError
from default_set.models import *
from django.utils import timezone
from default_set.transactions import UserTransaction
from main.discovers import PAYMENT_SYSTEMS
from decimal import *

deltas = {
    PLAN_PERIOD_HOUR: timezone.timedelta(hours=1),
    PLAN_PERIOD_DAY: timezone.timedelta(days=1),
    PLAN_PERIOD_WEEK: timezone.timedelta(weeks=1),
    PLAN_PERIOD_MONTH: timezone.timedelta(days=30),
}


class Command(BaseCommand):
    def handle(self, *args, **options):
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



