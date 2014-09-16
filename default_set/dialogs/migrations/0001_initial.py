# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Участники диалога')),
            ],
            options={
                'verbose_name_plural': 'Диалоги',
                'verbose_name': 'Диалог',
                'ordering': ('-id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DialogMessages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата содания')),
                ('message', models.TextField(verbose_name='Сообщение', max_length=500)),
                ('is_readed', models.BooleanField(default=False, verbose_name='Прочитано')),
                ('dialog', models.ForeignKey(to='dialogs.Dialog', verbose_name='Диалог')),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, default=None, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Сообщения в диалогах',
                'verbose_name': 'Сообщение в диалоге',
                'ordering': ('-created',),
            },
            bases=(models.Model,),
        ),
    ]
