import telegram
from asgiref.sync import async_to_sync
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes


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
