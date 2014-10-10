# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('default_set', '0004_plan_end_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='deposit_return',
            field=models.BooleanField(verbose_name='Возврат депозита после окончания', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.IntegerField(choices=[(1, 'Deposit'), (2, 'Withdrawal'), (3, 'Internal outgoing transfer'), (4, 'Internal incoming transfer'), (5, 'Referral commission'), (6, 'Accrual of interest'), (7, 'Admin earning'), (8, 'Возврат депозита')], null=True, verbose_name='Transaction type', db_index=True),
        ),
    ]
