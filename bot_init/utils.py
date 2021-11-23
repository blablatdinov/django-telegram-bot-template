import json
from datetime import datetime

from django.conf import settings
from django.utils.timezone import make_aware
from loguru import logger
from telebot import TeleBot

from bot_init.models import Message, Subscriber

log = logger.bind(task="app")


def save_message(msg):
    """Сохранение сообщения от пользователя."""
    date = make_aware(datetime.fromtimestamp(msg.date))
    from_user_id = msg.from_user.id
    message_id = msg.message_id
    chat_id = msg.chat.id
    text = msg.text
    try:
        json_str = msg.json
    except Exception as e:
        log.error(str(e))
        json_str = str(msg)
    json_text = json.dumps(json_str, indent=2, ensure_ascii=False)
    Message.objects.create(
        date=date, from_user_id=from_user_id, message_id=message_id,
        chat_id=chat_id, text=text, json=json_text
    )


def get_subscriber_by_chat_id(chat_id):
    """Получить подписчика по идентификатору чата."""
    try:
        subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
        return subscriber
    except Subscriber.DoesNotExist:
        log.error(f"subscriber with id {chat_id} does not exist")


def get_tbot_instance() -> TeleBot:
    """Получаем экземпляр класса TeleBot для удобной работы с API."""
    return TeleBot(settings.TG_BOT.token)


tbot = get_tbot_instance()


def tg_delete_message(chat_id, message_id):
    """Удалить сообщение в телеграм."""
    tbot.delete_message(chat_id=chat_id, message_id=message_id)
    log.info(f"delete message (id: {message_id}, chat_id: {chat_id}")
