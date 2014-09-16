from decimal import Decimal
import hashlib
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from . import NAME
from django.views.decorators.csrf import csrf_exempt
from default_set.models import *
from default_set.transactions import UserTransaction
from payment_systems.perfect_money.pm import PerfectMoney
from django.db import transaction
from django.utils.translation import ugettext_lazy as _


def deposit_continue(request, tr, context):
    return render(request, NAME + '/continue.html', context)


@csrf_exempt
def deposit_result(request):
    if not request.method == 'POST':
        return HttpResponse('no')

    outhash = hashlib.md5('{}:{}:{}:USD:{}:{}:{}:{}'.format(
        request.POST.get('PAYMENT_ID'),
        settings.PM_WALLET,
        request.POST.get('PAYMENT_AMOUNT'),
        request.POST.get('PAYMENT_BATCH_NUM'),
        request.POST.get('PAYER_ACCOUNT'),
        hashlib.md5(settings.PM_PASSPHRASE.encode('utf-8')).hexdigest().upper(),
        request.POST.get('TIMESTAMPGMT')).encode('utf-8')).hexdigest()

    if str(outhash).upper() == str(request.POST.get('V2_HASH')).upper():
        tr = Transaction.objects.get(pk=int(request.POST.get('PAYMENT_ID')))
        if tr.amount == Decimal(request.POST.get('PAYMENT_AMOUNT')) and tr.ps == NAME and not tr.is_ended:
            transaction = UserTransaction()
            transaction.do_transaction_deposit(tr.user, tr, request.POST['PAYMENT_BATCH_NUM'])

    return HttpResponse('ok')


@transaction.atomic
@user_passes_test(lambda u: u.is_superuser)
def transaction_withdraw(tr):
    tr = Transaction.objects.select_for_update().get(pk=tr.pk)
    if tr.transaction_type == TRANSACTION_WITHDRAW and not tr.is_ended:
        pm = PerfectMoney(settings.PM_ACCOUNT, settings.PM_PASSWORD)
        transfer = pm.transfer(settings.PM_WALLET, tr.get_wallet(), tr.get_abs_amount(),
                               settings.PROJECT_TITLE + ' withdrawal', tr.pk)
        tr.batch = transfer['PAYMENT_BATCH_NUM']
        tr.is_ended = True
        tr.save()
        tr.user.email_user(_('Вывод средств в проекте {}').format(settings.PROJECT_TITLE),
                           'mail/withdrawal_end.html', dict(transaction=tr))
