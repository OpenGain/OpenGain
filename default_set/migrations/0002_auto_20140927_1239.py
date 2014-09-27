# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('default_set', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='title_en',
            field=models.CharField(null=True, max_length=50, default='', verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plan',
            name='title_ru',
            field=models.CharField(null=True, max_length=50, default='', verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=30, db_index=True, unique=True, verbose_name='Login'),
        ),
    ]
