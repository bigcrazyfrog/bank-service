from django.contrib import admin

from app.internal.models.transaction import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'from_card', 'to_card', 'amount', 'date')
    readonly_fields = ('pk', 'from_card', 'to_card', 'amount', 'date')
