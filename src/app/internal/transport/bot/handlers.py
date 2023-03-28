import telegram
from asgiref.sync import sync_to_async, async_to_sync
from telegram import Update
from telegram.ext import ContextTypes

from app.internal.services.account_card_service import BankAccount, BankCard
from app.internal.services.user_service import User, log_errors

from . import static_text as st


def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    async_to_sync(context.bot.send_message)(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=telegram.constants.ParseMode.HTML,
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
