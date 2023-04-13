import re

from app.internal.models.account_card import Account, Card

RE_ACCOUNT = r'[0-9]{10}'
RE_CARD = r'[0-9]{16}'


class AccountService:
    @staticmethod
    def get_list(telegram_id):
        numbers = Account.objects.filter(user_profile__telegram_id=telegram_id).values('number')
        return list(map(lambda num: str(num['number']), numbers))

    @staticmethod
    def exist(number):
        try:
            Account.objects.get(number=number)
            return True
        except Account.DoesNotExist:
            return False

    @staticmethod
    def balance(telegram_id, number):
        rule = re.compile(RE_ACCOUNT)

        if not rule.search(number):
            raise ValueError

        try:
            account = Account.objects.get(owner__id=telegram_id, number=number)
            return account.balance
        except Account.DoesNotExist:
            return None

    @staticmethod
    def send_money(from_account, to_account, amount):
        account1 = Account.objects.get(number=from_account)
        account1.balance -= amount
        account1.save()

        account2 = Account.objects.get(number=to_account)
        account2.balance += amount
        account2.save()

    @staticmethod
    def send_money_by_id(from_account, by_id, amount):
        account = Account.objects.filter(owner__id=by_id)
        AccountService.send_money(from_account, account[0].number, amount)


class CardService:
    @staticmethod
    def get_list(telegram_id):
        card_numbers = Card.objects.filter(account__owner__id=telegram_id).values('number')
        return list(map(lambda num: str(num['number']), card_numbers))

    @staticmethod
    def get_account(number, telegram_id=None):
        try:
            if telegram_id is None:
                card = Card.objects.get(number=number)
            else:
                card = Card.objects.get(number=number, account__owner__id=telegram_id)

            return card.account
        except Card.DoesNotExist:
            return None
