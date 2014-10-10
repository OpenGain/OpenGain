# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deposits', '0001_initial'),
        ('default_set', '0002_auto_20140927_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='deposit',
            field=models.ForeignKey(null=True, verbose_name='Депозит', to='deposits.Deposit', related_name='deposit_transactions', blank=True),
            preserve_default=True,
        ),
    ]
