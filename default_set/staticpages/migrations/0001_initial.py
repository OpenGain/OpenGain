# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('url', models.CharField(verbose_name='URL', db_index=True, max_length=100)),
                ('title', models.CharField(verbose_name='title', max_length=200)),
                ('title_ru', models.CharField(null=True, verbose_name='title', max_length=200)),
                ('title_en', models.CharField(null=True, verbose_name='title', max_length=200)),
                ('content', models.TextField(blank=True, verbose_name='content')),
                ('content_ru', models.TextField(null=True, blank=True, verbose_name='content')),
                ('content_en', models.TextField(null=True, blank=True, verbose_name='content')),
                ('template_name', models.CharField(help_text="Example: 'staticpages/contact_page.html'. If this isn't provided, the system will use 'staticpages/default.html'.", verbose_name='template name', blank=True, max_length=70)),
            ],
            options={
                'verbose_name_plural': 'static pages',
                'ordering': ('url',),
                'verbose_name': 'static page',
            },
            bases=(models.Model,),
        ),
    ]
