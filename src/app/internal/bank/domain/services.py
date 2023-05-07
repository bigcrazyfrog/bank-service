from typing import List

from app.internal.bank.db.models import Account
from app.internal.bank.domain.entities import AccountListSchema, ErrorResponse, CardListSchema


class IAccountRepository:
    def get_list(self, user_id: str) -> AccountListSchema:
        ...

    def get_card_list(self, user_id: str) -> CardListSchema:
        ...

    def exists(self, number: int, user_id=None) -> bool:
        ...

    def get_balance(self, user_id: str, number: int) -> float:
        ...

    def send_money(self, user_id: str, from_account: int, to_account: int, amount: float) -> bool:
        ...

    def get_account_by_id(self, user_id: str) -> Account:
        ...

    def transaction_history(self, user_id: str, number: int, page: int):
        ...

    def interaction_list(self, user_id: str):
        ...


class AccountService:
    def __init__(self, account_repo: IAccountRepository):
        self._account_repo = account_repo

    def get_list(self, user_id: str) -> AccountListSchema:
        return self._account_repo.get_list(user_id=user_id)

    def get_card_list(self, user_id: str) -> CardListSchema:
        return self._account_repo.get_card_list(user_id=user_id)

    def exists(self, number: int, user_id=None) -> bool:
        return self._account_repo.exists(number=number, user_id=user_id)

    def get_balance(self, user_id: str, number: int) -> float:
        return self._account_repo.get_balance(user_id=user_id, number=number)

    def send_money(self, user_id: str, from_account: int, to_account: int, amount: float) -> bool:
        return self._account_repo.send_money(user_id, from_account, to_account, amount)

    def send_money_by_id(self, user_id: str, from_account: int, by_id: str, amount: float) -> bool:
        to_account = self._account_repo.get_account_by_id(user_id=by_id)
        return self._account_repo.send_money(user_id, from_account, to_account.number, amount)

    def transaction_history(self, user_id: str, number: int, page=0):
        return self._account_repo.transaction_history(user_id, number, page)

    def interaction_list(self, user_id: str):
        return self._account_repo.interaction_list(user_id=user_id)
