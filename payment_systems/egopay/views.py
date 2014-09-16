from django.shortcuts import render
from . import NAME
from default_set.models import *


def deposit_continue(request, pk):
    transaction = request.user.transactions.filter(pk=pk, transaction_type=TRANSACTION_DEPOSIT, is_ended=False)
    return render(request, NAME + '/continue.html', dict(transaction=transaction))