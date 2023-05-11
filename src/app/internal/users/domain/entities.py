from ninja import Schema
from pydantic import Field


class Tokens(Schema):
    access_token: str
    refresh_token: str


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
    password: str


class IncorrectPasswordError(Exception):
    pass


class NotFoundException(Exception):
    def __init__(self, name: str = "Object", id: str = "ID"):
        self.name = name
        self.id = id
