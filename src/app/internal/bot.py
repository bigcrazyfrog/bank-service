from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters

from config.settings import BOT_TOKEN

from .transport.bot.handlers import *

commands = [
    ('start', start),
    ('setphone', set_phone),
    ('me', me),
    ('balance', balance),
    ('accountlist', account_list),
    ('card_list', card_list),
    ('help', help)
]


def update_handlers(application):
    for command in commands:
        application.add_handler(CommandHandler(*command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("send_money", send_money)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, card_number_enter)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount_enter)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, translation_type)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, to_card)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, to_telegram_id)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, to_bank_account)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

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
        port=3228,
        url_path=BOT_TOKEN,
        webhook_url=f'https://nikita.backend23.2tapp.cc/{BOT_TOKEN}',
    )
