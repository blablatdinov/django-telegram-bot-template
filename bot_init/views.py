from time import sleep

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import telebot

from config.settings import TG_BOT
from bot_init.service import registration_subscriber
from bot_init.utils import save_message


token = TG_BOT.token
tbot = telebot.TeleBot(TG_BOT.token)
tbot.remove_webhook()
sleep(1)
web = tbot.set_webhook(f'{TG_BOT.webhook_host}/{TG_BOT.token}')


@csrf_exempt
def bot(request):
    """ Обработчик пакетов от телеграмма """
    if request.content_type == 'application/json':
        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        tbot.process_new_updates([update])
        return HttpResponse('')
    else:
        raise PermissionDenied


@tbot.message_handler(commands=['start'])  # Обработчик команды старт
def start_handler(message):
    """ Обработчик команды /start """
    save_message(message)
    registration_subscriber(message)
    ...
