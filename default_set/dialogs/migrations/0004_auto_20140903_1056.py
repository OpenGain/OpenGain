# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dialogs', '0003_auto_20140828_0643'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dialog',
            options={'verbose_name': 'Dialog', 'verbose_name_plural': 'Dialogs', 'ordering': ('-id',)},
        ),
        migrations.AlterField(
            model_name='dialogmessage',
            name='dialog',
            field=models.ForeignKey(to='dialogs.Dialog', verbose_name='Dialog', related_name='messages'),
        ),
    ]
