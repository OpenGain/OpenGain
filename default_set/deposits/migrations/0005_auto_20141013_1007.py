# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deposits', '0004_auto_20141013_1003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deposittransaction',
            old_name='deposit',
            new_name='deposit_fk',
        ),
        migrations.RenameField(
            model_name='deposittransaction',
            old_name='transaction',
            new_name='transaction_fk',
        ),
        migrations.RemoveField(
            model_name='deposit',
            name='transactions',
        ),
        migrations.AddField(
            model_name='deposit',
            name='transactions_deposit',
            field=models.ManyToManyField(verbose_name='Транзакции', to='deposits.DepositTransaction'),
            preserve_default=True,
        ),
    ]
