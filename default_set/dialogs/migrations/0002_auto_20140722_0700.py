# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dialogs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DialogMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата содания')),
                ('message', models.TextField(max_length=500, verbose_name='Сообщение')),
                ('is_readed', models.BooleanField(default=False, verbose_name='Прочитано')),
                ('dialog', models.ForeignKey(to='dialogs.Dialog', verbose_name='Диалог')),
                ('user', models.ForeignKey(null=True, default=None, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Сообщения в диалогах',
                'ordering': ('-created',),
                'verbose_name': 'Сообщение в диалоге',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='dialogmessages',
            name='dialog',
        ),
        migrations.RemoveField(
            model_name='dialogmessages',
            name='user',
        ),
        migrations.DeleteModel(
            name='DialogMessages',
        ),
    ]
