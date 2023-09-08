from abc import ABC, abstractmethod
from typing import Iterable

from django.db.models import QuerySet

from app.internal.bank.db.models import Account, Transaction
from app.internal.bank.domain.entities import AccountListSchema, CardListSchema


class IBankRepository(ABC):
    """Interface for bank repository."""

    @abstractmethod
    def get_account_list(self, user_id: str) -> AccountListSchema:
        ...

    @abstractmethod
    def get_card_list(self, user_id: str) -> CardListSchema:
        ...

    @abstractmethod
    def exists(self, number: int, user_id=None) -> bool:
        ...

    @abstractmethod
    def get_balance(self, user_id: str, number: int) -> float:
        ...

    @abstractmethod
    def send_money(self, user_id: str, from_account: int, to_account: int, amount: float, path: str) -> bool:
        ...

    @abstractmethod
    def get_account_by_id(self, user_id: str) -> Account:
        ...

    @abstractmethod
    def get_unseen_transaction(self, user_id: str, number: int, page: int):
        ...

    @abstractmethod
    def transaction_history(self, user_id: str, number: int, page: int):
        ...

    @abstractmethod
    def interaction_list(self, user_id: str):
        ...


class BankService:
    """Service contains business logic of Bank app."""

    def __init__(self, bank_repo: IBankRepository):
        self._bank_repo = bank_repo

    def get_account_list(self, user_id: str) -> AccountListSchema:
        """Get a list of existing user account numbers."""
        return self._bank_repo.get_account_list(user_id=user_id)

    def get_card_list(self, user_id: str) -> CardListSchema:
        """Get a card of existing user account numbers."""
        return self._bank_repo.get_card_list(user_id=user_id)

    def exists(self, number: int, user_id=None) -> bool:
        """Check if card is exist."""
        return self._bank_repo.exists(number=number, user_id=user_id)

    def get_balance(self, user_id: str, number: int) -> float:
        """Get card balance."""
        return self._bank_repo.get_balance(user_id=user_id, number=number)

    def send_money(self, user_id: str, from_account: int, to_account: int, amount: float, path: str) -> bool:
        """Provide to create new transaction.

        Args:
            user_id: Owner of card.
            from_account: Account through which money is transferred.
            to_account: Account where money is transferred to.
            amount: Transfer amount
            path: Path to postcard file in AWS S3 storage.

        Raises:
            ErrorResponse: If insufficient funds in the account.

        """
        return self._bank_repo.send_money(user_id, from_account, to_account, amount, path)

    def send_money_by_id(self, user_id: str, from_account: int, by_id: str, amount: float, path: str) -> bool:
        to_account = self._bank_repo.get_account_by_id(user_id=by_id)
        return self._bank_repo.send_money(user_id, from_account, to_account.number, amount, path)

    def transaction_history(self, user_id: str, number: int, page: int = 0) -> QuerySet[Transaction]:
        """Get lasted transaction history."""
        return self._bank_repo.transaction_history(user_id, number, page)

    def get_unseen_transaction(self, user_id: str, number: int, page=0) -> QuerySet[Transaction]:
        """Get actual transaction history."""
        return self._bank_repo.get_unseen_transaction(user_id, number, page)

    def interaction_list(self, user_id: str) -> Iterable[str]:
        """Get users to interact in all time."""
        return self._bank_repo.interaction_list(user_id=user_id)
