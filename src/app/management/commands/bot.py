from django.conf import settings
from django.core.management.base import BaseCommand

from app.internal import bot


class Command(BaseCommand):
    """Launch of Telegram bot."""

    help = "Run Telegram bot"

    def handle(self, *args, **options):
        """Telegram bot endpoint.

        If debug is true use polling, webhook with others.

        """
        if settings.DEBUG:
            bot.start_polling()
        else:
            bot.start_webhook()
