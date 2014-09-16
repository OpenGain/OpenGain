# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import payment_systems.perfect_money.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PSForUser',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('wallet', models.CharField(validators=[payment_systems.perfect_money.models.validate_pm_wallet], blank=True, verbose_name='Perfect Money wallet', null=True, max_length=8, db_index=True, default=None)),
                ('balance', models.DecimalField(max_digits=8, default=0, decimal_places=2, verbose_name='Balance')),
                ('user', models.OneToOneField(related_name='perfect_money', verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'perfect money',
                'verbose_name': 'perfect money',
            },
            bases=(models.Model,),
        ),
    ]
