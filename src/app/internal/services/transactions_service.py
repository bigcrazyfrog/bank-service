from app.internal.models.account_card import Account, Card
from app.internal.models.bank_transaction import BankTransaction
from app.internal.services.account_card_service import BankCard


class Transaction:
    @staticmethod
    def to_card(from_card, to_card, amount):
        try:
            BankCard.add_amount(from_card, -amount)
            BankCard.add_amount(to_card, amount)

            BankTransaction.objects.create(from_card=from_card, to_card=to_card, amount=amount)
            return 1

        except Card.DoesNotExist:
            return -1

    @staticmethod
    def to_bank_account(from_card, to_account_number, amount):
        to_card = Card.objects.filter(account__number=to_account_number)

        return Transaction.to_card(from_card, to_card[0].number, amount)

    @staticmethod
    def to_telegram_id(from_card, to_telegram_id, amount):
        to_card = Card.objects.filter(account__user_profile__telegram_id=to_telegram_id)

        return Transaction.to_card(from_card, to_card[0].number, amount)
