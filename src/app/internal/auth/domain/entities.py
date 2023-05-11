from ninja import Schema


class Tokens(Schema):
    access_token: str
    refresh_token: str


class AlreadyExistException(Exception):
    def __init__(self, name: str = "Object", id: str = "ID"):
        self.name = name
        self.id = id
