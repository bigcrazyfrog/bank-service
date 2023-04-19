from itertools import chain
from random import randint

from django.db import transaction
from django.db.models import F, Q

import re
from typing import List

from app.internal.models.account_card import Account, Card
from app.internal.models.admin_user import User
from app.internal.models.transaction import Transaction

RE_ACCOUNT = r'[0-9]{10}'
RE_CARD = r'[0-9]{16}'


class AccountService:
    @staticmethod
    def get_list(telegram_id: str) -> List[str]:
        return Account.objects.filter(owner__id=telegram_id).values_list('number', flat=True)

    @staticmethod
    def exist(number: int, telegram_id=None) -> bool:
        if telegram_id is None:
            return Account.objects.filter(number=number).exists()

        return Account.objects.filter(owner__id=telegram_id, number=number).exists()

    @staticmethod
    def balance(telegram_id: str, number: int) -> float:
        rule = re.compile(RE_ACCOUNT)

        if not rule.search(number):
            raise ValueError

        try:
            account = Account.objects.get(owner__id=telegram_id, number=number)
            return account.balance
        except Account.DoesNotExist:
            raise ValueError

    @staticmethod
    def create_first(telegram_id: str) -> Account | None:
        rand_number = randint(10 ** 10, 10 ** 11)
        while Account.objects.filter(number=rand_number).exists():
            rand_number = randint(10 ** 10, 10 ** 11)

        user = User.objects.get(id=telegram_id)
        return Account.objects.create(number=rand_number, owner=user)

    @staticmethod
    @transaction.non_atomic_requests()
    def send_money(from_account: int, to_account: int, amount: float) -> None:
        if from_account == to_account:
            raise Exception("similar account")

        account1 = Account.objects.get(number=from_account)
        account2 = Account.objects.get(number=to_account)

        account1.balance = F('balance') - amount
        account2.balance = F('balance') + amount

        account1.save(update_fields=('balance',))
        account2.save(update_fields=('balance',))

        Transaction.objects.create(from_account=account1, to_account=account2, amount=amount)

    @staticmethod
    def send_money_by_id(from_account: int, by_id: str, amount: float) -> None:
        account = Account.objects.filter(owner__id=by_id).values('number')
        AccountService.send_money(from_account, account[0].number, amount)

    @staticmethod
    def transaction_history(telegram_id: str, number: int, page=1):
        try:
            account = Account.objects.get(owner__id=telegram_id, number=number)
        except:
            raise ValueError

        return Transaction.objects.filter(Q(from_account=account) | Q(to_account=account))\
            .order_by('-date')

    @staticmethod
    def interaction_list(telegram_id: str):
        incoming = Transaction.objects.filter(from_account__owner__id=telegram_id)\
            .values_list('to_account__owner__name', flat=True).distinct()

        outgoing = Transaction.objects.filter(to_account__owner__id=telegram_id)\
            .values_list('from_account__owner__name', flat=True).distinct()

        return set(chain(incoming, outgoing))


class CardService:
    @staticmethod
    def get_list(telegram_id: str) -> List[str]:
        return Card.objects.filter(account__owner__id=telegram_id).values_list('number', flat=True)

    @staticmethod
    def get_account(number: int, telegram_id=None) -> Card:
        try:
            if telegram_id is None:
                card = Card.objects.get(number=number)
            else:
                card = Card.objects.get(number=number, account__owner__id=telegram_id)

            return card.account
        except Card.DoesNotExist:
            return None

    @staticmethod
    def create_first(telegram_id: str) -> Card | None:
        if Card.objects.filter(account__owner__id=telegram_id).exists():
            return None

        rand_number = randint(10 ** 16, 10 ** 17)
        while Card.objects.filter(number=rand_number).exists():
            rand_number = randint(10 ** 16, 10 ** 17)

        account = AccountService.create_first(telegram_id)
        return Card.objects.create(number=rand_number, account=account)
