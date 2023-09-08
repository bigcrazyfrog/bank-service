from asgiref.sync import sync_to_async
from django.http import HttpRequest
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

import app.internal.responses.static_text as st
from app.internal.bank.domain.entities import AccountListSchema, BalanceSchema, CardListSchema
from app.internal.bank.domain.services import BankService
from app.internal.responses.services import log_errors, send_message
from app.internal.storage.db.repositories import StorageRepository
from app.internal.users.db.exceptions import NotFoundException
from app.internal.users.domain.entities import SuccessResponse


class BankHandlers:
    """Bank handlers for REST API."""

    def __init__(self, bank_service: BankService, storage_service: StorageRepository):
        self._bank_service = bank_service
        self._storage_service = storage_service

    def get_account_list(self, request: HttpRequest) -> AccountListSchema:
        """Get a list of accounts which the user has."""
        return self._bank_service.get_account_list(user_id=request.user)

    def get_card_list(self, request: HttpRequest) -> CardListSchema:
        """Get a list of cards which the user has."""
        return self._bank_service.get_card_list(user_id=request.user)

    def get_balance(self, request: HttpRequest, number: int) -> BalanceSchema:
        """Get balance of card."""
        balance = self._bank_service.get_balance(user_id=request.user, number=number)
        return BalanceSchema(balance=balance)

    def send_money(self, request: HttpRequest, from_account: int, to_account: int, amount: float) -> SuccessResponse:
        """Create new money transaction."""
        success = self._bank_service.send_money(user_id=request.user, from_account=from_account,
                                                to_account=to_account, amount=amount)

        return SuccessResponse(success=success)

    def send_money_by_id(self, request: HttpRequest, from_account: int, by_id: str, amount: float) -> SuccessResponse:
        success = self._bank_service.send_money_by_id(user_id=request.user, from_account=from_account,
                                                      by_id=by_id, amount=amount)
        return SuccessResponse(success=success)


class BotBankHandlers:
    """Bank handlers for Telegram bot.

    Contain sync methods for interaction with bank by Telegram bot API.

    """

    def __init__(self, account_service: BankService, storage_service: StorageRepository):
        self._account_service = account_service
        self._storage_service = storage_service

    @log_errors
    def get_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send current balance of account."""
        try:
            user_id = update.effective_chat.id
            number = context.args[0]

            balance = self._account_service.get_balance(user_id=user_id, number=number)
            text = st.balance + str(balance)
        except (IndexError, ValueError, NotFoundException):
            text = st.account_not_find

        send_message(update, context, text)

    @log_errors
    def get_account_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a list of existing account numbers which the user has."""
        accounts = self._account_service.get_account_list(update.effective_chat.id)
        account_numbers = accounts.accounts

        text = st.balance_not_exist
        if account_numbers:
            text = st.account_list + '\n'.join([str(number) for number in account_numbers])

        send_message(update, context, text)

    @log_errors
    def get_card_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a list of existing card numbers which the user has."""
        cards = self._account_service.get_card_list(update.effective_chat.id)
        card_numbers = cards.cards

        text = st.balance_not_exist
        if card_numbers:
            text = st.account_list + '\n'.join([str(number) for number in card_numbers])

        send_message(update, context, text)

    @log_errors
    def send_money(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Starting point of money transaction.

        Start with choosing the account through which the transaction will take place.

        """
        accounts = self._account_service.get_account_list(update.effective_chat.id)

        reply_keyboard = []
        for account in accounts.accounts:
            reply_keyboard.append([str(account)])

        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        context.user_data["last_keyboard"] = markup

        send_message(update, context, st.choose_card, markup)
        return 0

    @log_errors
    def card_number_enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handler use after choosing the account.

        Validate input account. Send message with choosing amount of money.

        """
        account_number = update.message.text

        try:
            account_number = int(account_number)
        except ValueError:
            send_message(update, context, st.incorrect_input, context.user_data["last_keyboard"])
            return 0

        account = self._account_service.exists(account_number, update.effective_chat.id)
        if not account:
            send_message(update, context, st.not_found, context.user_data["last_keyboard"])
            return 0

        context.user_data["from_account"] = account_number
        send_message(update, context, st.enter_amount)

        return 1

    @log_errors
    def amount_enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Validate amount input. Send message with choosing type of translation."""
        amount = update.message.text

        try:
            amount = int(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            send_message(update, context, st.incorrect_input)
            return 1

        if amount > self._account_service.get_balance(update.effective_chat.id, context.user_data["from_account"]):
            send_message(update, context, st.no_money)
            return 1

        context.user_data["amount"] = amount

        reply_keyboard = [["🆔 Telegram ID", "📝 Счет в банке"]]

        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        context.user_data["last_keyboard"] = markup

        send_message(update, context, st.transaction_type, markup)
        return 2

    @log_errors
    def translation_type(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Accepts translation type."""
        match update.message.text:
            case "🆔 Telegram ID":
                context.user_data["transaction_type"] = "to_telegram_id"
                send_message(update, context, st.send_to_telegram_id)
                return 4
            case "📝 Счет в банке":
                context.user_data["transaction_type"] = "to_bank_account"
                send_message(update, context, st.send_to_bank_account)
                return 5

        send_message(update, context, st.incorrect_input, context.user_data["last_keyboard"])
        return 2

    @log_errors
    def to_telegram_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Wait telegram ID for transaction."""
        context.user_data["to_telegram_id"] = update.message.text

        reply_keyboard = [["Без открытки"]]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        send_message(update, context, st.send_postcard, markup=markup)
        return 6

    @log_errors
    def to_bank_account(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Wait account number to continue transaction."""
        try:
            context.user_data["to_bank_account"] = int(update.message.text)
            if not self._account_service.exists(int(update.message.text)):
                raise ValueError
        except Exception:
            send_message(update, context, st.incorrect_account)
            return 5

        reply_keyboard = [["Без открытки"]]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        send_message(update, context, st.send_postcard, markup)
        return 6

    @log_errors
    def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancellation of the transaction.

        Clear previous steps. User returns to the main menu.

        """
        context.user_data.clear()
        send_message(update, context, st.cancelled)

        return ConversationHandler.END

    @log_errors
    async def attach_picture(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Async attach a postcard to transaction.

        The final stage of the transaction. Validate and save input postcard.
        Send money by the chosen method.

        """
        path = None
        if update.message.text != "Без открытки":
            file = await context.bot.get_file(update.message.photo[-1].file_id)
            buf = bytearray()
            await file.download_as_bytearray(buf)

            path = self._storage_service.create(buf)

        if context.user_data["transaction_type"] == "to_telegram_id":
            await sync_to_async(self._account_service.send_money_by_id)(
                update.effective_chat.id,
                context.user_data["from_account"],
                context.user_data["to_telegram_id"],
                context.user_data["amount"],
                path,
            )
        else:
            await sync_to_async(self._account_service.send_money)(
                update.effective_chat.id,
                context.user_data["from_account"],
                context.user_data["to_bank_account"],
                context.user_data["amount"],
                path,
            )

        await context.bot.send_message(chat_id=update.effective_chat.id, text=st.successful)
        return ConversationHandler.END

    @log_errors
    def transaction_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send all lasted transaction history."""
        text = st.interaction_not_found
        try:
            account = context.args[0]
            history = self._account_service.transaction_history(update.effective_chat.id, account)

            text = st.transaction_history(history, account)
        except (IndexError, ValueError):
            pass

        send_message(update, context, text)

    @log_errors
    def get_unseen_transaction(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send history of previously unseen transactions."""
        text = st.interaction_not_found
        try:
            account = context.args[0]
            history = self._account_service.get_unseen_transaction(update.effective_chat.id, account)

            text = st.transaction_history(history, account)
        except (IndexError, ValueError):
            pass

        send_message(update, context, text)

    @log_errors
    def interaction_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a list of users who have recently had an interaction with."""
        text = st.interaction_not_found

        interactions = self._account_service.interaction_list(update.effective_chat.id)
        if len(interactions) != 0:
            text = st.interaction_list
            for i, user in enumerate(interactions):
                text += f'{i + 1}. {user}\n'

        send_message(update, context, text)
