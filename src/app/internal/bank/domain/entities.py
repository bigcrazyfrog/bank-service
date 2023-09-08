from ninja import Schema


class AccountListSchema(Schema):
    """Account list schema."""
    accounts: list


class CardListSchema(Schema):
    """Card list schema."""
    cards: list


class BalanceSchema(Schema):
    """Balance schema."""
    balance: float
