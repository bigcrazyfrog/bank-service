from asgiref.sync import sync_to_async
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters

from app.internal.bank.db.repositories import AccountRepository
from app.internal.bank.domain.services import AccountService
from app.internal.bank.presentation.bot_handlers import BotAccountHandlers
from app.internal.users.db.repositories import UserRepository
from app.internal.users.presentation.bot_handlers import *
from config.settings import BOT_PORT, BOT_TOKEN, BOT_WEBHOOK_HOST


def update_handlers(application):
    user_repo = UserRepository()
    user_service = UserService(user_repo=user_repo)
    bot_user_handler = BotUserHandlers(user_service=user_service)

    application.add_handler(CommandHandler("start", sync_to_async(bot_user_handler.start)))
    application.add_handler(CommandHandler("set_phone", sync_to_async(bot_user_handler.set_phone)))
    application.add_handler(CommandHandler("me", sync_to_async(bot_user_handler.me)))
    application.add_handler(CommandHandler("help", sync_to_async(bot_user_handler.help)))
    application.add_handler(CommandHandler("favorite_list", sync_to_async(bot_user_handler.favorite_list)))
    application.add_handler(CommandHandler("add_favorite", sync_to_async(bot_user_handler.add_favorite)))
    application.add_handler(CommandHandler("remove_favorite", sync_to_async(bot_user_handler.remove_favorite)))
    application.add_handler(CommandHandler("set_password", sync_to_async(bot_user_handler.set_password)))

    account_repo = AccountRepository()
    account_service = AccountService(account_repo=account_repo)
    bot_account_handler = BotAccountHandlers(account_service=account_service)

    application.add_handler(CommandHandler("balance", sync_to_async(bot_account_handler.get_balance)))
    application.add_handler(CommandHandler("account_list", sync_to_async(bot_account_handler.get_list)))
    application.add_handler(CommandHandler("card_list", sync_to_async(bot_account_handler.get_card_list)))
    application.add_handler(CommandHandler("interaction_list", sync_to_async(bot_account_handler.interaction_list)))
    application.add_handler(CommandHandler("history", sync_to_async(bot_account_handler.transaction_history)))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("send_money", sync_to_async(bot_account_handler.send_money))],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, sync_to_async(bot_account_handler.card_number_enter))],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, sync_to_async(bot_account_handler.amount_enter))],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, sync_to_async(bot_account_handler.translation_type))],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, sync_to_async(bot_account_handler.to_telegram_id))],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, sync_to_async(bot_account_handler.to_bank_account))],
        },
        fallbacks=[CommandHandler("cancel", sync_to_async(bot_account_handler.cancel))],
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
        port=BOT_PORT,
        url_path=BOT_TOKEN,
        webhook_url=f'https://{BOT_WEBHOOK_HOST}/{BOT_TOKEN}',
    )
