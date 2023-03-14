from telegram.ext import ApplicationBuilder, CommandHandler

from config.settings import BOT_TOKEN

from .transport.bot.handlers import *


def update_handlers(application):
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('setphone', set_phone))
    application.add_handler(CommandHandler('me', me))

    return application


def bot_polling():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    update_handlers(application)

    application.run_polling()
