import re

from asgiref.sync import sync_to_async

from app.internal.models.account_card import Account, Card

RE_ACCOUNT = r'[0-9]{10}'
RE_CARD = r'[0-9]{16}'


@sync_to_async
def account_list(telegram_id):
    numbers = Account.objects.filter(telegram_id=telegram_id).values('number')
    return list(map(lambda num: str(num['number']), numbers))


@sync_to_async
def account_balance(telegram_id, number):
    rule = re.compile(RE_ACCOUNT)

    if not rule.search(number):
        raise ValueError

    try:
        account = Account.objects.get(telegram_id=telegram_id, number=number)
        return account.balance
    except Account.DoesNotExist:
        return None


@sync_to_async
def card_list(telegram_id):
    account_numbers = Account.objects.filter(telegram_id=telegram_id).values('number')
    card_numbers = Card.objects.filter(account_number__in=account_numbers).values('number')

    return list(map(lambda num: str(num['number']), card_numbers))


@sync_to_async
def card_balance(telegram_id, number):
    rule = re.compile(RE_CARD)

    if not rule.search(number):
        raise ValueError

    try:
        card = Card.objects.get(number=number)
        if card.account_number.telegram_id != telegram_id:
            return None

        return card.balance
    except (Card.DoesNotExist, Account.DoesNotExist):
        return None
