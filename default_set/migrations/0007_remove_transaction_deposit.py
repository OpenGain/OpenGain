# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('default_set', '0006_auto_20141013_0950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='deposit',
        ),
    ]
