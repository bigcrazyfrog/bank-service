from telegram.ext import ApplicationBuilder, CommandHandler

from config.settings import BOT_TOKEN

from .transport.bot.handlers import *


def update_handlers(application):
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('setphone', set_phone))
    application.add_handler(CommandHandler('me', me))
    application.add_handler(CommandHandler('accountbalance', get_account_balance))
    application.add_handler(CommandHandler('accountlist', get_account_list))
    application.add_handler(CommandHandler('cardlist', get_card_list))
    application.add_handler(CommandHandler('cardbalance', get_card_balance))

    return application


def bot_polling():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    update_handlers(application)

    application.run_polling()
