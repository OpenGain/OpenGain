from django.contrib import admin
from .models import *
from main import opengain_admin
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(News, site=opengain_admin)
class NewsAdmin(TabbedTranslationAdmin):
    list_display = ('created', 'title', 'is_public')
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ('is_public', )
