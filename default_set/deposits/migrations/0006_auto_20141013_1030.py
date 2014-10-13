# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('default_set', '0007_remove_transaction_deposit'),
        ('deposits', '0005_auto_20141013_1007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deposittransaction',
            name='deposit_fk',
        ),
        migrations.RemoveField(
            model_name='deposittransaction',
            name='transaction_fk',
        ),
        migrations.RemoveField(
            model_name='deposit',
            name='transactions_deposit',
        ),
        migrations.DeleteModel(
            name='DepositTransaction',
        ),
        migrations.AddField(
            model_name='deposit',
            name='transactions',
            field=models.ManyToManyField(to='default_set.Transaction', verbose_name='Транзакции'),
            preserve_default=True,
        ),
    ]
