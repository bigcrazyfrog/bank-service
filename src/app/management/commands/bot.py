from django.core.management.base import BaseCommand

from app.internal.bot import bot_polling


class Command(BaseCommand):
    help = 'bot'

    def handle(self, *args, **options):
        bot_polling()
