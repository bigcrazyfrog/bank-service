from app.internal.models.account_card import Account, Card
from app.internal.models.transaction import Transaction
from app.internal.services.account_card_service import CardService


class TransactionService:
    @staticmethod
    def to_card(from_card, to_card, amount):
        try:
            CardService.add_amount(from_card, -amount)
            CardService.add_amount(to_card, amount)

            Transaction.objects.create(from_card=from_card, to_card=to_card, amount=amount)
            return 1

        except Card.DoesNotExist:
            return -1

    @staticmethod
    def to_bank_account(from_card, to_account_number, amount):
        to_card = Card.objects.filter(account__number=to_account_number)

        return TransactionService.to_card(from_card, to_card[0].number, amount)

    @staticmethod
    def to_telegram_id(from_card, to_telegram_id, amount):
        to_card = Card.objects.filter(account__user_profile__telegram_id=to_telegram_id)

        return TransactionService.to_card(from_card, to_card[0].number, amount)
