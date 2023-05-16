from ninja import Schema
from pydantic import Field


class AccountListSchema(Schema):
    accounts: list


class CardListSchema(Schema):
    cards: list


class BalanceSchema(Schema):
    balance: float
