from typing import List

from django.http import JsonResponse, HttpRequest
from ninja.params import Path, Body

from app.internal.bank.domain.entities import BalanceSchema, SuccessResponse, AccountListSchema
from app.internal.bank.domain.services import AccountService


class AccountHandlers:
    def __init__(self, account_service: AccountService):
        self._account_service = account_service

    def get_list(self, request) -> AccountListSchema:
        return self._account_service.get_list(user_id=request.user)

    def exists(self, request, number: int) -> SuccessResponse:
        success = self._account_service.exists(number=number, user_id=request.user)
        return SuccessResponse(success=success)

    def get_balance(self, request, number: int) -> BalanceSchema:
        balance = self._account_service.get_balance(user_id=request.user, number=number)
        return BalanceSchema(balance=balance)

    def send_money(self, request, from_account: int, to_account: int, amount: float) -> SuccessResponse:
        success = self._account_service.send_money(user_id=request.user, from_account=from_account,
                                                   to_account=to_account, amount=amount)
        return SuccessResponse(success=success)

    def send_money_by_id(self, request, from_account: int, by_id: str, amount: float) -> SuccessResponse:
        success = self._account_service.send_money_by_id(user_id=request.user, from_account=from_account,
                                                         by_id=by_id, amount=amount)
        return SuccessResponse(success=success)
