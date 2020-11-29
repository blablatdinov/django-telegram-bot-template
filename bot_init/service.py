import time

from telebot import TeleBot
from telebot.apihelper import ApiException
from django.conf import settings
from loguru import logger
from bot_init.utils import get_tbot_instance

from bot_init.models import Subscriber
from bot_init.schemas import SUBSCRIBER_ACTIONS
from bot_init.services.answer import Answer
from bot_init.utils import save_message

log = logger.bind(task="app")
tbot = get_tbot_instance()


def registration_subscriber(chat_id: int):
    """Логика сохранения подписчика"""
    subscriber, created = Subscriber.objects.get_or_create(tg_chat_id=chat_id)
    ...


def check_user_status_by_typing(chat_id: int):
    sub = get_subscriber_by_chat_id(chat_id)
    try:
        tbot.send_chat_action(sub.tg_chat_id, 'typing')
        if not sub.is_active:
            sub.is_active = True
            sub.save(update_fields=['is_active'])
        return True
    except Exception as e:
        service_api_exception(e)


def count_active_users():
    count = 0
    for sub in pbar(Subscriber.objects.all()):
        if check_user_status_by_typing(sub.tg_chat_id):
            count += 1
    return count


def service_api_exception(exception):
    if ('bot was blocked by the user' in str(e) or 'user is deactivated' in str(e)) and sub.is_active:
        _subscriber_unsubscribed(sub.tg_chat_id)


def send_answer(answer: Answer, chat_id):
    tbot.send_message(chat_id, Answer.text)


def do_mailing(data: dict):
    for chat_id, text in data.items():
        try:
            answer = Answer(text)
            message_instance = send_answer(answer, chat_id)
            save_message(message_instance)
        except ApiException as e:
            service_api_exception(e)


def create_action(subscriber: Subscriber, action: str):
    """Создаем запись в БД о подписке, отписке или реактивации бота пользователем"""
    SubscriberAction.objects.create(subscriber=subscriber, action=action)


def update_webhook(host=f'{settings.TG_BOT.webhook_host}/{settings.TG_BOT.token}'):
    """Обновляем webhook"""
    try:
        tbot.remove_webhook()
        res = tbot.set_webhook(host)
        log.info("webhook updated successfully")
    except ApiException as e:
        log.error(e)


def _subscriber_unsubscribed(chat_id: int):
    """Действия, выполняемые при блокировке бота пользователем"""
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    subscriber.is_active = False
    subscriber.save()
    _create_action(subscriber, SUBSCRIBER_ACTIONS[1][0])


def _not_created_subscriber_service(subscriber: Subscriber):
    """Фунция вызывается если пользователь, который уже существует отправил команду /start"""
    if subscriber.is_active:
        # Пользователь уже подписан
        return Answer(...)
    # Пользователь отписался и подписался вновь
    _create_action(subscriber, SUBSCRIBER_ACTIONS[2][0])
    subscriber.is_active = True
    subscriber.save(update_fields=['is_active'])
    return Answer(...)


def _created_subscriber_service(subscriber: Subscriber) -> Answer:
    """Функция обрабатывает и генерирует ответ для нового подписчика"""
    start_message_text = AdminMessage.objects.get(key='start').text  # TODO создать это сообщение с миграцией
    _create_action(subscriber, SUBSCRIBER_ACTIONS[0][0])
    send_message_to_admin(
        f'Зарегестрировался новый пользователь'
    )
    answers = ...
    return answers
