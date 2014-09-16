from django.contrib import admin
from .models import *
from main import opengain_admin


@admin.register(Ticket, site=opengain_admin)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'created', 'is_closed')
    list_editable = ('is_closed',)
    list_filter = ('is_closed',)
    search_fields = ('user__username',)


@admin.register(TicketMessage, site=opengain_admin)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'created', 'user', 'message', 'is_readed')
    list_editable = ('is_readed',)
    search_fields = ('user__username',)
    list_filter = ('is_readed',)
