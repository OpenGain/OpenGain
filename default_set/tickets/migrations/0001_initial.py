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
            name='Ticket',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Create date')),
                ('subject', models.CharField(verbose_name='Subject', max_length=100)),
                ('is_closed', models.BooleanField(default=False, verbose_name='Closed')),
                ('user', models.ForeignKey(related_name='tickets', verbose_name='User', to=settings.AUTH_USER_MODEL, null=True, default=None)),
            ],
            options={
                'verbose_name_plural': 'tickets',
                'ordering': ('-created',),
                'verbose_name': 'ticket',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketMessage',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('message', models.TextField(verbose_name='Message', max_length=500)),
                ('is_readed', models.BooleanField(default=False, verbose_name='Read')),
                ('ticket', models.ForeignKey(related_name='messages', verbose_name='Ticket', to='tickets.Ticket')),
                ('user', models.ForeignKey(related_name='tickets_messages', verbose_name='User', to=settings.AUTH_USER_MODEL, null=True, default=None)),
            ],
            options={
                'verbose_name_plural': 'tickets messages',
                'ordering': ('-created',),
                'verbose_name': 'tickets message',
            },
            bases=(models.Model,),
        ),
    ]
