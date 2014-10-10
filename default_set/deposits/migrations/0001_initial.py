# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('default_set', '0002_auto_20140927_1239'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', default=django.utils.timezone.now)),
                ('last_update', models.DateTimeField(auto_now_add=True, verbose_name='Changed', auto_now=True, default=django.utils.timezone.now)),
                ('ps', models.CharField(verbose_name='Payment System', choices=[('perfect_money', 'Perfect Money'), ('payeer', 'Payeer')], db_index=True, null=True, max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Amount', default=0)),
                ('accrued', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Начислено', default=0)),
                ('is_ended', models.BooleanField(db_index=True, verbose_name='Completed', default=False)),
                ('plan', models.ForeignKey(verbose_name='План', to='default_set.Plan', related_name='plan_deposits')),
                ('user', models.ForeignKey(null=True, verbose_name='User', to=settings.AUTH_USER_MODEL, related_name='deposits')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
