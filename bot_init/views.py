import telebot
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from loguru import logger

from bot_init.service import registration_subscriber
from bot_init.utils import get_tbot_instance, save_message
from config.settings import TG_BOT

token = TG_BOT.token
tbot = get_tbot_instance()

log = logger.bind(task="write_in_data")


@csrf_exempt
def bot(request):
    """Обработчик пакетов от телеграмма."""
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
    """Обработчик команды /start."""
    save_message(message)
    registration_subscriber(message.chat.id)
    tbot.send_message(message.chat.id, 'hello')
