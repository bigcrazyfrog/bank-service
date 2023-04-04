import telegram
from asgiref.sync import async_to_sync, sync_to_async
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from app.internal.services.account_card_service import BankAccount, BankCard
from app.internal.services.user_service import User, log_errors
from app.internal.services.transactions_service import Transaction

from . import static_text as st
from ...models.account_card import Card, Account
from ...models.favorite_user import FavoriteUser


def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, markup=None):
    if markup is None:
        markup = ReplyKeyboardRemove()

    async_to_sync(context.bot.send_message)(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_markup=markup,
    )


@log_errors
@sync_to_async
def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    User.new_user(telegram_id=update.effective_chat.id)

    send_message(update, context, st.welcome)


@log_errors
@sync_to_async
def set_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = st.success

    try:
        User.update_phone(update.effective_chat.id, context.args[0])
    except (IndexError, ValueError):
        text = st.incorrect

    send_message(update, context, text)


@log_errors
@sync_to_async
def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = User.info(update.effective_chat.id)

    number = user['phone_number']
    text = st.info + st.line
    text += f'🆔 Telegram ID : {update.effective_chat.id}\n 📞 Ваш номер : {number}' + st.line

    if number is None:
        text = st.not_exist

    send_message(update, context, text)


@log_errors
@sync_to_async
def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = st.account_not_find
    try:
        card_balance = BankCard.balance(update.effective_chat.id, context.args[0])

        if not (card_balance is None):
            text = st.balance + str(card_balance)
    except (IndexError, ValueError):
        text = st.incorrect

    send_message(update, context, text)


@log_errors
@sync_to_async
def account_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    numbers = BankAccount.get_list(update.effective_chat.id)
    text = st.balance_not_exist

    if numbers:
        text = st.account_list + '\n'.join(numbers)

    send_message(update, context, text)


@log_errors
@sync_to_async
def card_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    numbers = BankCard.get_list(update.effective_chat.id)

    text = st.balance_not_exist

    if numbers:
        text = st.account_list + '\n'.join(numbers)

    send_message(update, context, text)


@log_errors
@sync_to_async
def send_money(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        FavoriteUser.objects.get(profile__telegram_id=update.effective_chat.id)
    except FavoriteUser.DoesNotExist:
        send_message(update, context, st.no_access)
        return ConversationHandler.END

    cards = BankCard.get_list(update.effective_chat.id)

    reply_keyboard = []
    for card in cards:
        reply_keyboard.append([card])

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    context.user_data["last_keyboard"] = markup

    send_message(update, context, st.choose_card, markup)
    return 0


@log_errors
@sync_to_async
def card_number_enter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    card = update.message.text

    try:
        int(card)
    except Exception:
        send_message(update, context, st.incorrect_card, context.user_data["last_keyboard"])
        return 0

    if not BankCard.is_exist(card, update.effective_chat.id):
        send_message(update, context, st.not_found, context.user_data["last_keyboard"])
        return 0

    context.user_data["from_card"] = card
    send_message(update, context, st.enter_amount)

    return 1


@log_errors
@sync_to_async
def amount_enter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    amount = update.message.text

    try:
        amount = int(amount)
        if amount <= 0:
            raise ValueError
    except Exception:
        send_message(update, context, st.incorrect_card)
        return 1

    if amount > BankCard.balance(update.effective_chat.id, context.user_data["from_card"]):
        send_message(update, context, st.no_money)
        return 1

    context.user_data["amount"] = amount

    reply_keyboard = [["Telegram ID", "Bank account"],
                      ["Card number"]]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    context.user_data["last_keyboard"] = markup

    send_message(update, context, st.transaction_type, markup)
    return 2


@log_errors
@sync_to_async
def translation_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match update.message.text:
        case "Telegram ID":
            send_message(update, context, st.send_to_telegram_id)
            return 4
        case "Bank account":
            send_message(update, context, st.send_to_bank_account)
            return 5
        case "Card number":
            send_message(update, context, st.send_to_card_number)
            return 3

    send_message(update, context, st.incorrect_card, context.user_data["last_keyboard"])
    return 2


@log_errors
@sync_to_async
def to_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    card = update.message.text
    if not BankCard.is_exist(card):
        send_message(update, context, st.not_found)
        return 3

    if card == context.user_data["from_card"]:
        send_message(update, context, st.pitiful_attempt)
        return 3

    try:
        bank_card = Card.objects.get(number=update.message.text)
        FavoriteUser.objects.get(profile__telegram_id=bank_card.account.user_profile.telegram_id)

    except FavoriteUser.DoesNotExist:
        send_message(update, context, st.not_in_favorite)
        return ConversationHandler.END

    transaction = Transaction.to_card(context.user_data["from_card"], card,
                                      context.user_data["amount"])

    send_message(update, context, "Готово")
    return ConversationHandler.END


@log_errors
@sync_to_async
def to_telegram_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.text
    try:
        FavoriteUser.objects.get(profile__telegram_id=telegram_id)

    except FavoriteUser.DoesNotExist:
        send_message(update, context, st.not_in_favorite)
        return ConversationHandler.END

    transaction = Transaction.to_telegram_id(context.user_data["from_card"],
                                             telegram_id, context.user_data["amount"])

    send_message(update, context, st.success)
    return ConversationHandler.END


@log_errors
@sync_to_async
def to_bank_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    account = update.message.text

    if not BankAccount.is_exist(account):
        send_message(update, context, st.incorrect_account)
        return 5

    try:
        bank_account = Account.objects.get(number=account)
        FavoriteUser.objects.get(profile__telegram_id=bank_account.user_profile.telegram_id)

    except FavoriteUser.DoesNotExist:
        send_message(update, context, st.pitiful_attempt)
        return ConversationHandler.END

    try:
        Transaction.to_bank_account(context.user_data["from_card"],
                                    update.message.text, context.user_data["amount"])

        send_message(update, context, st.success)
    except Exception:
        send_message(update, context, st.error)

    return ConversationHandler.END


@log_errors
@sync_to_async
def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    send_message(update, context, st.cancelled)

    return ConversationHandler.END
