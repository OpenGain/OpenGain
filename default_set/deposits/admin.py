from django.contrib import admin
from .models import Deposit
from main import opengain_admin

class DepositTransactionInline(admin.TabularInline):
    model = Deposit.transactions.through
    raw_id_fields = ['transaction', ]

@admin.register(Deposit, site=opengain_admin)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('created', 'last_update', 'user', 'ps', 'plan', 'amount', 'is_ended')
    raw_id_fields = ('user', 'plan',)
    exclude = ('transactions',)
    inlines = [
        DepositTransactionInline,
               ]

