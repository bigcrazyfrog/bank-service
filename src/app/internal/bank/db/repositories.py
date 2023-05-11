from itertools import chain
from typing import List, Optional

from django.db import transaction
from django.db.models import F, Q

from app.internal.bank.db.models import Account, Card, Transaction
from app.internal.bank.domain.entities import AccountListSchema, CardListSchema, ErrorResponse
from app.internal.bank.domain.services import IBankRepository
from app.internal.users.domain.entities import NotFoundException

BATCH_SIZE: int = 10


class BankRepository(IBankRepository):
    def get_account_list(self, user_id: str) -> AccountListSchema:
        accounts = Account.objects.filter(owner__id=user_id).values_list('number', flat=True)
        return AccountListSchema(accounts=list(accounts))

    def get_card_list(self, user_id: str) -> CardListSchema:
        cards = Card.objects.filter(account__owner__id=user_id).values_list('number', flat=True)
        return CardListSchema(cards=list(cards))

    def exists(self, number: int, user_id=None) -> bool:
        if user_id is None:
            return Account.objects.filter(number=number).exists()

        return Account.objects.filter(owner__id=user_id, number=number).exists()

    def get_balance(self, user_id: str, number: int) -> float:
        account = Account.objects.filter(owner__id=user_id, number=number).first()

        if account is None:
            raise NotFoundException(name="Account", id=str(number))

        return account.balance

    def send_money(self, user_id: str, from_account: int, to_account: int, amount: float) -> bool:
        if from_account == to_account:
            raise Exception("similar account")

        with transaction.atomic():
            account1 = Account.objects.filter(owner__id=user_id, number=from_account).first()
            account2 = Account.objects.filter(number=to_account).first()

            if account1 is None:
                raise NotFoundException(name="account", id=from_account)
            if account2 is None:
                raise NotFoundException(name="account", id=to_account)

            if account1.balance < amount:
                raise ErrorResponse(error="Недостаточно средств")

            account1.balance = F('balance') - amount
            account2.balance = F('balance') + amount

            account1.save(update_fields=('balance',))
            account2.save(update_fields=('balance',))

        Transaction.objects.create(from_account=account1, to_account=account2, amount=amount)
        return True

    def get_account_by_id(self, user_id: str) -> Account:
        account = Account.objects.filter(owner__id=user_id).first()
        if account is None:
            raise NotFoundException(name="User", id=user_id)
        return account

    def transaction_history(self, user_id: str, number: int, page: int):
        account = Account.objects.filter(owner__id=user_id, number=number).first()
        if account is None:
            raise NotFoundException(name="account", id=number)

        return Transaction.objects.filter(Q(from_account=account) | Q(to_account=account)) \
                   .select_related("from_account", "to_account") \
                   .order_by('-date')[BATCH_SIZE * page: BATCH_SIZE * (page + 1)]

    def interaction_list(self, user_id: str):
        incoming = Transaction.objects.filter(from_account__owner__id=user_id) \
            .values_list('to_account__owner__name', flat=True).distinct()

        outgoing = Transaction.objects.filter(to_account__owner__id=user_id) \
            .values_list('from_account__owner__name', flat=True).distinct()

        return set(chain(incoming, outgoing))
