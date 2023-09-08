from ninja import Schema
from pydantic import Field


class Tokens(Schema):
    """Auth token schema."""
    access_token: str
    refresh_token: str


class SuccessResponse(Schema):
    """Success response schema."""
    success: bool = False


class ErrorResponse(Schema):
    """Error response schema."""
    error: str = "error"


class UserSchema(Schema):
    """General user schema."""
    id: str = Field(max_length=225)
    name: str = Field(max_length=225)


class UserOut(UserSchema):
    """Out user schema."""
    phone_number: str = None


class UserIn(UserSchema):
    """Incoming user schema."""
    password: str
