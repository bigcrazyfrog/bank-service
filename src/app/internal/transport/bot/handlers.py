import telegram
from asgiref.sync import async_to_sync, sync_to_async
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from app.internal.services.account_card_service import AccountService, CardService
from app.internal.services.user_service import UserService, log_errors

from . import static_text as st


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
    UserService.new_user(telegram_id=update.effective_chat.id)

    send_message(update, context, st.welcome)


@log_errors
@sync_to_async
def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    send_message(update, context, st.help)


@log_errors
@sync_to_async
def set_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = st.success

    try:
        UserService.update_phone(update.effective_chat.id, context.args[0])
    except (IndexError, ValueError):
        text = st.incorrect

    send_message(update, context, text)


@log_errors
@sync_to_async
def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = UserService.info(update.effective_chat.id)

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
        account_balance = AccountService.balance(update.effective_chat.id, context.args[0])

        if not (account_balance is None):
            text = st.balance + str(account_balance)
    except (IndexError, ValueError):
        text = st.incorrect

    send_message(update, context, text)


@log_errors
@sync_to_async
def account_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    numbers = AccountService.get_list(update.effective_chat.id)
    text = st.balance_not_exist

    if numbers:
        text = st.account_list + '\n'.join(numbers)

    send_message(update, context, text)


@log_errors
@sync_to_async
def card_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    numbers = CardService.get_list(update.effective_chat.id)

    text = st.balance_not_exist

    if numbers:
        text = st.account_list + '\n'.join(numbers)

    send_message(update, context, text)


@log_errors
@sync_to_async
def send_money(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cards = CardService.get_list(update.effective_chat.id)

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
    card_number = update.message.text

    try:
        int(card_number)
    except Exception:
        send_message(update, context, st.incorrect_input, context.user_data["last_keyboard"])
        return 0

    account = CardService.get_account(card_number, update.effective_chat.id)
    if account is None:
        send_message(update, context, st.not_found, context.user_data["last_keyboard"])
        return 0

    context.user_data["from_account"] = str(account.number)
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
        send_message(update, context, st.incorrect_input)
        return 1

    if amount > AccountService.balance(update.effective_chat.id, context.user_data["from_account"]):
        send_message(update, context, st.no_money)
        return 1

    context.user_data["amount"] = amount

    reply_keyboard = [["🆔 Telegram ID", "📝 Счет в банке"],
                      ["💳 Номер карты"]]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    context.user_data["last_keyboard"] = markup

    send_message(update, context, st.transaction_type, markup)
    return 2


@log_errors
@sync_to_async
def translation_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match update.message.text:
        case "🆔 Telegram ID":
            send_message(update, context, st.send_to_telegram_id)
            return 4
        case "📝 Счет в банке":
            send_message(update, context, st.send_to_bank_account)
            return 5
        case "💳 Номер карты":
            send_message(update, context, st.send_to_card_number)
            return 3

    send_message(update, context, st.incorrect_input, context.user_data["last_keyboard"])
    return 2


@log_errors
@sync_to_async
def to_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    account = CardService.get_account(update.message.text)
    if account is None:
        send_message(update, context, st.not_found)
        return 3

    if account.number == context.user_data["from_account"]:
        send_message(update, context, st.pitiful_attempt)
        return 3

    try:
        AccountService.send_money(context.user_data["from_account"], account.number,
                                  context.user_data["amount"])

        send_message(update, context, st.successful)
    except Exception:
        print(Exception)
        send_message(update, context, st.error)

    return ConversationHandler.END


@log_errors
@sync_to_async
def to_telegram_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.text

    try:
        AccountService.send_money_by_id(context.user_data["from_account"],
                                        telegram_id, context.user_data["amount"])

        send_message(update, context, st.successful)
        return ConversationHandler.END
    except Exception:
        send_message(update, context, st.user_not_fount)
        return 4


@log_errors
@sync_to_async
def to_bank_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    account = update.message.text

    if not AccountService.exist(account):
        send_message(update, context, st.incorrect_account)
        return 5

    try:
        AccountService.send_money(context.user_data["from_account"],
                                  update.message.text, context.user_data["amount"])

        send_message(update, context, st.successful)
    except Exception:
        send_message(update, context, st.error)

    return ConversationHandler.END


@log_errors
@sync_to_async
def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    send_message(update, context, st.cancelled)

    return ConversationHandler.END


@log_errors
@sync_to_async
def favorite_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    favorite_users = UserService.get_favorite_list(update.effective_chat.id)

    if favorite_users:
        text = st.favorite_list + '\n'.join(favorite_users)
    else:
        text = st.favorite_no_list

    send_message(update, context, text)


@log_errors
@sync_to_async
def add_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = st.user_not_found

    try:
        if UserService.add_favorite(update.effective_chat.id, context.args[0]):
            text = st.user_was_add
    except IndexError:
        text = st.incorrect_input

    send_message(update, context, text)


@log_errors
@sync_to_async
def remove_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = st.user_not_found

    try:
        if UserService.remove_favorite(update.effective_chat.id, context.args[0]):
            text = st.user_was_remove
    except IndexError:
        text = st.incorrect_input

    send_message(update, context, text)
