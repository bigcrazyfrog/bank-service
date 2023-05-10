from ninja import Schema
from pydantic import Field


class AccountListSchema(Schema):
    accounts: list


class CardListSchema(Schema):
    cards: list


class BalanceSchema(Schema):
    balance: float


class SuccessResponse(Schema):
    success: bool = False


class ErrorResponse(Schema):
    error: str = "error"


class NotFoundException(Exception):
    def __init__(self, name: str = "Object", id: str = "ID"):
        self.name = name
        self.id = id
