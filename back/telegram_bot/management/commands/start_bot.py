from django.core.management.base import BaseCommand
from telegram_bot.main_bot import main


class Command(BaseCommand):

    help = 'Запуск бота'

    def handle(self, *args, **options):
        main()
