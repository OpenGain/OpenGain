from django.contrib import admin
from .models import StaticPage
from django.utils.translation import ugettext_lazy as _
from .forms import StaticpageForm
from main import opengain_admin
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(StaticPage, site=opengain_admin)
class StaticPageAdmin(TabbedTranslationAdmin):
    form = StaticpageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content')}),
        (_('Дополнительные параметры'), {'classes': ('collapse',), 'fields': ('template_name', )}),
    )
    list_display = ('url', 'title')
    search_fields = ('url', 'title')

