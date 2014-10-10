# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('default_set', '0003_transaction_deposit'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='end_period',
            field=models.IntegerField(default=24, blank=True, verbose_name='Срок в часах', null=True),
            preserve_default=True,
        ),
    ]
