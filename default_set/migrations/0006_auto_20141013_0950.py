# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('default_set', '0005_auto_20141010_0409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.IntegerField(verbose_name='Transaction type', db_index=True, null=True, choices=[(1, 'Deposit'), (2, 'Withdrawal'), (3, 'Internal outgoing transfer'), (4, 'Internal incoming transfer'), (5, 'Referral commission'), (6, 'Accrual of interest'), (8, 'Возврат депозита')]),
        ),
    ]
