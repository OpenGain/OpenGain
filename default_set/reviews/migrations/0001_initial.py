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
            name='Review',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('review', models.TextField(verbose_name='Review', max_length=500)),
                ('admin_answer', models.TextField(null=True, verbose_name='Admin answer', blank=True, max_length=500)),
                ('is_public', models.BooleanField(default=False, verbose_name='Public')),
                ('user', models.ForeignKey(related_name='reviews', verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'reviews',
                'ordering': ('-pk',),
                'verbose_name': 'review',
            },
            bases=(models.Model,),
        ),
    ]
