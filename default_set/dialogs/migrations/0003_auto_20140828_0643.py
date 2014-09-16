# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dialogs', '0002_auto_20140722_0700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialog',
            name='users',
            field=models.ManyToManyField(related_name='dialogs', to=settings.AUTH_USER_MODEL, verbose_name='Участники диалога'),
        ),
        migrations.AlterField(
            model_name='dialogmessage',
            name='dialog',
            field=models.ForeignKey(verbose_name='Диалог', related_name='messages', to='dialogs.Dialog'),
        ),
        migrations.AlterField(
            model_name='dialogmessage',
            name='user',
            field=models.ForeignKey(default=None, verbose_name='Пользователь', related_name='dialog_messages', null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
