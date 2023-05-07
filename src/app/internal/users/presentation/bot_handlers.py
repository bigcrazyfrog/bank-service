import telegram
from asgiref.sync import async_to_sync, sync_to_async
from django.core.exceptions import ValidationError
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from app.internal.users.domain.services import UserService
from app.internal.users.presentation import static_text as st
from app.internal.users.domain.entities import UserIn


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'error {e}')
            raise e

    return inner


def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, markup=None) -> None:
    if markup is None:
        markup = ReplyKeyboardRemove()

    async_to_sync(context.bot.send_message)(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_markup=markup,
    )


class BotUserHandlers:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    @log_errors
    def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = UserIn(
            id=update.effective_chat.id,
            name=update.effective_chat.first_name,
        )

        self._user_service.add_user(user)
        send_message(update, context, st.welcome)

    @log_errors
    def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        send_message(update, context, st.help)

    @log_errors
    def set_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = st.success

        try:
            self._user_service.update_phone(update.effective_chat.id, context.args[0])
        except (IndexError, ValidationError):
            text = st.incorrect

        send_message(update, context, text)

    @log_errors
    def me(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = self._user_service.get_user_by_id(update.effective_chat.id)

        text = st.me(user)
        send_message(update, context, text)

    @log_errors
    def favorite_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        favorite_users = self._user_service.get_favorite_list(update.effective_chat.id)

        if favorite_users:
            text = st.favorite_list + '\n'.join(favorite_users)
        else:
            text = st.favorite_no_list

        send_message(update, context, text)

    @log_errors
    def add_favorite(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = st.user_not_found

        try:
            self._user_service.add_favorite(update.effective_chat.id, context.args[0])
            text = st.user_was_add
        except IndexError:
            text = st.incorrect_input

        send_message(update, context, text)

    @log_errors
    def remove_favorite(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = st.user_not_found

        try:
            self._user_service.remove_favorite(update.effective_chat.id, context.args[0])
            text = st.user_was_remove
        except IndexError:
            text = st.incorrect_input

        send_message(update, context, text)

    @log_errors
    def set_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            self._user_service.set_password(update.effective_chat.id, context.args[0])
            text = st.password_was_recorded
        except (IndexError, ValueError):
            text = st.incorrect_input

        send_message(update, context, text)
