from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters

from config.settings import BOT_TOKEN

from .transport.bot.handlers import *

commands = [
    ('start', sync_to_async(start)),
    ('set_phone', sync_to_async(set_phone)),
    ('me', sync_to_async(me)),
    ('balance', sync_to_async(balance)),
    ('account_list', sync_to_async(account_list)),
    ('card_list', sync_to_async(card_list)),
    ('help', sync_to_async(help)),
    ('favorite_list', sync_to_async(favorite_list)),
    ('add_favorite', sync_to_async(add_favorite)),
    ('remove_favorite', sync_to_async(remove_favorite)),
    ('history', sync_to_async(transaction_history)),
    ('interaction', sync_to_async(interaction_list)),
    ('create_account', sync_to_async(create_first_account)),
]


def update_handlers(application):
    for command in commands:
        application.add_handler(CommandHandler(*command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("send_money", sync_to_async(send_money))],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, sync_to_async(card_number_enter))],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, sync_to_async(amount_enter))],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, sync_to_async(translation_type))],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, sync_to_async(to_card))],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, sync_to_async(to_telegram_id))],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, sync_to_async(to_bank_account))],
        },
        fallbacks=[CommandHandler("cancel", sync_to_async(cancel))],
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
