from django.core.management.base import BaseCommand

from app.internal.bot import bot_polling, bot_webhook


class Command(BaseCommand):
    help = 'bot'

    def handle(self, *args, **options):
        bot_webhook()
