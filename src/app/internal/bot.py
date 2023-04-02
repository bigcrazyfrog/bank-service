from telegram.ext import ApplicationBuilder, CommandHandler

from config.settings import BOT_TOKEN

from .transport.bot.handlers import *

commands = [
    ('start', start),
    ('setphone', set_phone),
    ('me', me),
    ('balance', balance),
    ('accountlist', account_list),
    ('cardlist', card_list),
]


def update_handlers(application):
    for command in commands:
        application.add_handler(CommandHandler(*command))

    return application


def bot_polling():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    update_handlers(application)

    application.run_polling()


def bot_webhook():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    update_handlers(application)

    application.run_webhook(
        listen='0.0.0.0',
        port=8443,
        url_path='TOKEN',
        webhook_url='https://127.0.0.1:8443/TOKEN/',
    )
