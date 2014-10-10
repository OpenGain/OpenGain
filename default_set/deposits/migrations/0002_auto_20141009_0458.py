# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deposits', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deposit',
            options={'verbose_name_plural': 'Deposits', 'ordering': ('-id',), 'verbose_name': 'Депозит'},
        ),
        migrations.RemoveField(
            model_name='deposit',
            name='accrued',
        ),
    ]
