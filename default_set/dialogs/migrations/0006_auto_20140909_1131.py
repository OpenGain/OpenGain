# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dialogs', '0005_auto_20140908_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialog',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='dialogs', verbose_name='Interlocutors'),
        ),
    ]
