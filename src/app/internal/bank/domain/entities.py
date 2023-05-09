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


class UserSchema(Schema):
    id: str = Field(max_length=225)
    name: str = Field(max_length=225)


class UserOut(UserSchema):
    phone_number: str = None


class UserIn(UserSchema):
    ...


class FavouriteListSchema(Schema):
    favorite_user: list


class NotFoundException(Exception):
    def __init__(self, name: str = "Object", id: str = "ID"):
        self.name = name
        self.id = id
