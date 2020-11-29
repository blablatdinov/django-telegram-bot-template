from time import sleep

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from loguru import logger
import telebot

from config.settings import TG_BOT
from bot_init.service import registration_subscriber
from bot_init.utils import save_message, get_tbot_instance


token = TG_BOT.token
tbot = get_tbot_instance()

log = logger.bind(task="in_data")


@csrf_exempt
def bot(request):
    """Обработчик пакетов от телеграмма"""
    if request.content_type == 'application/json':
        json_data = request.body.decode('utf-8')
        log.info(json_data)
        update = telebot.types.Update.de_json(json_data)
        tbot.process_new_updates([update])
        return HttpResponse('')
    else:
        raise PermissionDenied


@tbot.message_handler(commands=['start'])
def start_handler(message):
    """Обработчик команды /start"""
    save_message(message)
    registration_subscriber(message.chat.id)
    ...
