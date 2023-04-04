from django.contrib import admin

from app.internal.models.bank_transaction import BankTransaction


@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'from_card', 'to_card', 'amount', 'date')
    readonly_fields = ('pk', 'from_card', 'to_card', 'amount', 'date')
