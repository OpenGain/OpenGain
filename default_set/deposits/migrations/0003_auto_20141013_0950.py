# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('default_set', '0006_auto_20141013_0950'),
        ('deposits', '0002_auto_20141009_0458'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('transaction', models.ForeignKey(verbose_name='Транзакция', to='default_set.Transaction')),
            ],
            options={
                'verbose_name': 'Транзакция депозита',
                'verbose_name_plural': 'Транзакции депозитов',
                'ordering': ('-id',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='deposit',
            name='transactions',
            field=models.ManyToManyField(verbose_name='Транзакции', to='deposits.DepositTransaction'),
            preserve_default=True,
        ),
    ]
