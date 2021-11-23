from django.urls import path

from bot_init.views import bot
from config.settings import TG_BOT

urlpatterns = [
    path(f'bot_init/{TG_BOT.token}', bot)
]
