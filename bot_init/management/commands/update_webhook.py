import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from bot_init.service import update_webhook


class Command(BaseCommand):
    help = 'command for update webhook'

    def handle(self, *args, **options):
        load_dotenv('.env')
        update_webhook(f'{os.getenv("HOST")}/bot_init/{os.getenv("BOT_TOKEN")}')
