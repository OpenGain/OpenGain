from django.contrib import admin
from .models import *
from main import opengain_admin


@admin.register(Dialog, site=opengain_admin)
class DialogAdmin(admin.ModelAdmin):
    raw_id_fields = ['users']


@admin.register(DialogMessage, site=opengain_admin)
class DialogMessageAdmin(admin.ModelAdmin):
    list_display = ('dialog', 'user', 'created', 'message', 'is_readed')
    list_editable = ('is_readed',)
    search_fields = ('user__username',)
    list_filter = ('is_readed',)
