import re

from app.internal.models.account_card import Account, Card

RE_ACCOUNT = r'[0-9]{10}'
RE_CARD = r'[0-9]{16}'


class BankAccount:
    @staticmethod
    def get_list(telegram_id):
        numbers = Account.objects.filter(user_profile__telegram_id=telegram_id).values('number')
        return list(map(lambda num: str(num['number']), numbers))

    @staticmethod
    def is_exist(number):
        try:
            Account.objects.get(number=number)
            return True
        except Account.DoesNotExist:
            return False


class CardService:
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

    @staticmethod
    def is_exist(number, telegram_id=None):
        try:
            if telegram_id is None:
                Card.objects.get(number=number)
            else:
                Card.objects.get(number=number, account__user_profile__telegram_id=telegram_id)

            return True
        except Card.DoesNotExist:
            return False

    @staticmethod
    def cheak_amount(number, amount):
        card = Card.objects.get(number=number)
        return card.balance >= amount

    @staticmethod
    def add_amount(number, amount):
        card = Card.objects.get(number=number)
        card.balance += amount
        card.save(update_fields=["balance"])
