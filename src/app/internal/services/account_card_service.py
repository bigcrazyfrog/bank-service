import re
from asgiref.sync import sync_to_async

from app.internal.models.account_card import Account, Card

RE_ACCOUNT = r'[0-9]{10}'
RE_CARD = r'[0-9]{16}'


class BankAccount:
    @staticmethod
    def get_list(telegram_id):
        numbers = Account.objects.filter(user_profile__telegram_id=telegram_id).values('number')
        return list(map(lambda num: str(num['number']), numbers))


class BankCard:
    @staticmethod
    def get_list(telegram_id):
        card_numbers = Card.objects.filter(account__user_profile__telegram_id=telegram_id).values('number')
        return list(map(lambda num: str(num['number']), card_numbers))

    @staticmethod
    def balance(telegram_id, number):
        rule = re.compile(RE_ACCOUNT)

        if not rule.search(number):
            raise ValueError

        try:
            card = Card.objects.get(account__user_profile__telegram_id=telegram_id, number=number)
            return card.balance
        except Card.DoesNotExist:
            return None



