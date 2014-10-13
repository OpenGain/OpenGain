# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deposits', '0003_auto_20141013_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposittransaction',
            name='deposit',
            field=models.ForeignKey(default=None, to='deposits.Deposit', null=True, verbose_name='Депозит'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='deposit',
            name='transactions',
            field=models.ManyToManyField(verbose_name='Транзакции', to='deposits.DepositTransaction', related_name='transaction_deposits'),
        ),
    ]
