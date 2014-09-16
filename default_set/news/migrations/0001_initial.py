# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('title', models.CharField(default='', unique=True, verbose_name='Title', max_length=100)),
                ('title_ru', models.CharField(default='', unique=True, null=True, verbose_name='Title', max_length=100)),
                ('title_en', models.CharField(default='', unique=True, null=True, verbose_name='Title', max_length=100)),
                ('slug', models.CharField(default='', unique=True, verbose_name='Link', max_length=100)),
                ('text', models.TextField(verbose_name='News body', max_length=5000)),
                ('text_ru', models.TextField(null=True, verbose_name='News body', max_length=5000)),
                ('text_en', models.TextField(null=True, verbose_name='News body', max_length=5000)),
                ('is_public', models.BooleanField(default=False, verbose_name='Public')),
            ],
            options={
                'verbose_name_plural': 'news',
                'ordering': ('-pk',),
                'verbose_name': 'news',
            },
            bases=(models.Model,),
        ),
    ]
