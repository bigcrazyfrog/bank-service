from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, ContextTypes

from app.internal.bank.domain.entities import AccountListSchema, CardListSchema, BalanceSchema
from app.internal.bank.domain.services import BankService
from app.internal.responses.services import send_message, log_errors
import app.internal.responses.static_text as st
from app.internal.users.db.exceptions import NotFoundException
from app.internal.users.domain.entities import SuccessResponse


class BankHandlers:
    def __init__(self, bank_service: BankService):
        self._bank_service = bank_service

    def get_account_list(self, request) -> AccountListSchema:
        return self._bank_service.get_account_list(user_id=request.user)

    def get_card_list(self, request) -> CardListSchema:
        return self._bank_service.get_card_list(user_id=request.user)

    def get_balance(self, request, number: int) -> BalanceSchema:
        balance = self._bank_service.get_balance(user_id=request.user, number=number)
        return BalanceSchema(balance=balance)

    def send_money(self, request, from_account: int, to_account: int, amount: float) -> SuccessResponse:
        success = self._bank_service.send_money(user_id=request.user, from_account=from_account,
                                                to_account=to_account, amount=amount)

        return SuccessResponse(success=success)

    def send_money_by_id(self, request, from_account: int, by_id: str, amount: float) -> SuccessResponse:
        success = self._bank_service.send_money_by_id(user_id=request.user, from_account=from_account,
                                                      by_id=by_id, amount=amount)
        return SuccessResponse(success=success)


class BotBankHandlers:
    def __init__(self, account_service: BankService):
        self._account_service = account_service

    @log_errors
    def get_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user_id = update.effective_chat.id
            number = context.args[0]

            balance = self._account_service.get_balance(user_id=user_id, number=number)
            text = st.balance + str(balance)
        except (IndexError, ValueError, NotFoundException):
            text = st.account_not_find

        send_message(update, context, text)

    @log_errors
    def get_account_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        accounts = self._account_service.get_account_list(update.effective_chat.id)
        account_numbers = accounts.accounts

        text = st.balance_not_exist
        if account_numbers:
            text = st.account_list + '\n'.join([str(number) for number in account_numbers])

        send_message(update, context, text)

    @log_errors
    def get_card_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        cards = self._account_service.get_card_list(update.effective_chat.id)
        card_numbers = cards.cards

        text = st.balance_not_exist
        if card_numbers:
            text = st.account_list + '\n'.join([str(number) for number in card_numbers])

        send_message(update, context, text)

    @log_errors
    def send_money(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        accounts = self._account_service.get_account_list(update.effective_chat.id)

        reply_keyboard = []
        for account in accounts.accounts:
            reply_keyboard.append([str(account)])

        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        context.user_data["last_keyboard"] = markup

        send_message(update, context, st.choose_card, markup)
        return 0

    @log_errors
    def card_number_enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        account_number = update.message.text

        try:
            account_number = int(account_number)
        except Exception:
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
    def amount_enter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        amount = update.message.text

        try:
            amount = int(amount)
            if amount <= 0:
                raise ValueError
        except Exception:
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
    def translation_type(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        match update.message.text:
            case "🆔 Telegram ID":
                send_message(update, context, st.send_to_telegram_id)
                return 4
            case "📝 Счет в банке":
                send_message(update, context, st.send_to_bank_account)
                return 5

        send_message(update, context, st.incorrect_input, context.user_data["last_keyboard"])
        return 2

    @log_errors
    def to_telegram_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.message.text

        try:
            self._account_service.send_money_by_id(update.effective_chat.id,
                                                   context.user_data["from_account"],
                                                   telegram_id, context.user_data["amount"])

            send_message(update, context, st.successful)
            return ConversationHandler.END
        except Exception as e:
            if str(e) == "similar account":
                send_message(update, context, st.pitiful_attempt)
            else:
                send_message(update, context, st.user_not_fount)
            return 4

    @log_errors
    def to_bank_account(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        account = update.message.text

        try:
            if not self._account_service.exists(int(account)):
                raise ValueError
        except Exception:
            send_message(update, context, st.incorrect_account)
            return 5

        try:
            self._account_service.send_money(update.effective_chat.id,
                                             context.user_data["from_account"],
                                             update.message.text, context.user_data["amount"])

            send_message(update, context, st.successful)
        except Exception as e:
            if str(e) == "similar account":
                send_message(update, context, st.pitiful_attempt)
            else:
                send_message(update, context, st.error)
                print(e)

        return ConversationHandler.END

    @log_errors
    def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data.clear()
        send_message(update, context, st.cancelled)

        return ConversationHandler.END

    @log_errors
    def transaction_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = st.interaction_not_found
        try:
            account = context.args[0]
            history = self._account_service.transaction_history(update.effective_chat.id, account)

            text = st.transaction_history(history, account)
        except (IndexError, ValueError):
            pass

        send_message(update, context, text)

    @log_errors
    def interaction_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = st.interaction_not_found

        interactions = self._account_service.interaction_list(update.effective_chat.id)
        if len(interactions) != 0:
            text = st.interaction_list
            for i, user in enumerate(interactions):
                text += f'{i + 1}. {user}\n'

        send_message(update, context, text)
