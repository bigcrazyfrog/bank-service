import telegram
from asgiref.sync import async_to_sync
from telegram import ReplyKeyboardRemove, Update
from telegram._utils.types import ReplyMarkup
from telegram.ext import ContextTypes


def log_errors(f):
    """Custom logger used console output."""
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"error {e}")
            raise e

    return inner


def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, markup: ReplyMarkup = None) -> None:
    """Use this method to send text messages.

    Args:
        update: Object represents an incoming update.
        context: Gathered customizable types.
        text: Your text for message.
        markup: Message markup for reply keyboard.

    Raises:
        telegram.error.TelegramError: As default telegram error.

    """
    if markup is None:
        markup = ReplyKeyboardRemove()

    async_to_sync(context.bot.send_message)(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_markup=markup,
    )
