from ninja import Schema


class Tokens(Schema):
    """Refresh token schema."""
    access_token: str
    refresh_token: str
