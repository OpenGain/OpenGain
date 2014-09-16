# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dialogs', '0004_auto_20140903_1056'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dialogmessage',
            options={'verbose_name': 'Message in the dialog', 'verbose_name_plural': 'Messages in the dialogs', 'ordering': ('-created',)},
        ),
        migrations.AlterField(
            model_name='dialogmessage',
            name='created',
            field=models.DateTimeField(verbose_name='Created', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='dialogmessage',
            name='is_readed',
            field=models.BooleanField(verbose_name='Read', default=False),
        ),
        migrations.AlterField(
            model_name='dialogmessage',
            name='message',
            field=models.TextField(verbose_name='Message', max_length=500),
        ),
        migrations.AlterField(
            model_name='dialogmessage',
            name='user',
            field=models.ForeignKey(verbose_name='User', default=None, null=True, to=settings.AUTH_USER_MODEL, related_name='dialog_messages'),
        ),
    ]
