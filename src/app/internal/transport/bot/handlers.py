import telegram
from telegram import Update
from telegram.ext import ContextTypes

from app.internal.services.account_card_service import account_balance, account_list, card_balance, card_list
from app.internal.services.user_service import info, log_errors, new_user, update_phone

from . import static_text as st


@log_errors
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await new_user(update.effective_chat.id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=st.welcome,
        parse_mode=telegram.constants.ParseMode.HTML,
    )


@log_errors
async def set_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = st.success

    try:
        await update_phone(update.effective_chat.id, context.args[0])
    except (IndexError, ValueError):
        text = st.incorrect

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )


@log_errors
async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await info(update.effective_chat.id)

    number = user['phone_number']
    text = st.info + st.line
    text += f'🆔 Telegram ID : {update.effective_chat.id}\n 📞 Ваш номер : {number}' + st.line

    if number is None:
        text = st.not_exist

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=telegram.constants.ParseMode.HTML,
    )


@log_errors
async def get_account_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = st.account_not_find
    try:
        balance = await account_balance(update.effective_chat.id, context.args[0])

        if not (balance is None):
            text = st.balance + str(balance)
    except (IndexError, ValueError):
        text = st.incorrect

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=telegram.constants.ParseMode.HTML,
    )


@log_errors
async def get_account_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    numbers = await account_list(update.effective_chat.id)
    text = st.balance_not_exist

    if numbers:
        text = st.account_list + '\n'.join(numbers)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=telegram.constants.ParseMode.HTML,
    )


@log_errors
async def get_card_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    numbers = await card_list(update.effective_chat.id)

    text = ''

    if numbers:
        text = st.account_list + '\n'.join(numbers)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=telegram.constants.ParseMode.HTML,
    )


@log_errors
async def get_card_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = st.account_not_find
    try:
        balance = await card_balance(update.effective_chat.id, context.args[0])

        if balance:
            text = st.balance + str(balance)
    except (IndexError, ValueError):
        text = st.incorrect

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=telegram.constants.ParseMode.HTML,
    )
