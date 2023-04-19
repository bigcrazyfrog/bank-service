from django.contrib import admin

from app.internal.models.transaction import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('from_account', 'to_account', 'amount', 'date',)
    readonly_fields = ('from_account', 'to_account', 'amount', 'date',)
