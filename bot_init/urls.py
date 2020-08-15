from django.urls import path

from config.settings import TG_BOT
from bot_init.views import bot


urlpatterns = [
    path(f'bot_init/{TG_BOT.token}', bot)
]
