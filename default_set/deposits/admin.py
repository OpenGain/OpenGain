from django.contrib import admin
from .models import Deposit
from main import opengain_admin


@admin.register(Deposit, site=opengain_admin)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('created', 'last_update', 'user', 'ps', 'plan', 'amount', 'is_ended')
    raw_id_fields=('user', 'plan',)