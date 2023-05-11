from typing import List, Tuple

from django.http import HttpRequest, JsonResponse
from ninja.params import Body, Path

from app.internal.bank.domain.entities import AccountListSchema, CardListSchema, BalanceSchema, SuccessResponse, \
    ErrorResponse
from app.internal.bank.domain.services import BankService


class BankHandlers:
    def __init__(self, bank_service: BankService):
        self._bank_service = bank_service

    def get_account_list(self, request) -> AccountListSchema:
        return self._bank_service.get_account_list(user_id=request.user)

    def get_card_list(self, request) -> CardListSchema:
        return self._bank_service.get_card_list(user_id=request.user)

    def get_balance(self, request, number: int) -> BalanceSchema:
        balance = self._bank_service.get_balance(user_id=request.user, number=number)
        return BalanceSchema(balance=balance)

    def send_money(self, request, from_account: int, to_account: int, amount: float) -> SuccessResponse:
        success = self._bank_service.send_money(user_id=request.user, from_account=from_account,
                                                to_account=to_account, amount=amount)

        return SuccessResponse(success=success)

    def send_money_by_id(self, request, from_account: int, by_id: str, amount: float) -> SuccessResponse:
        success = self._bank_service.send_money_by_id(user_id=request.user, from_account=from_account,
                                                      by_id=by_id, amount=amount)
        return SuccessResponse(success=success)
