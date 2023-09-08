from django.contrib import admin

from app.internal.bank.db.models import Account, Card, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Register `Account` model in admin panel."""


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    """Register `Card` model in admin panel."""


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Register `Transaction` model in admin panel."""
