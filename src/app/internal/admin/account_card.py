from django.contrib import admin

from app.internal.models.account_card import Account, Card


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'number', 'owner', 'balance')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('pk', 'number', 'account')
