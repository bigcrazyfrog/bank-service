from ninja import Schema


class Tokens(Schema):
    access_token: str
    refresh_token: str
