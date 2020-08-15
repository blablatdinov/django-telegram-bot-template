import time

from telebot import TeleBot
from django.conf import settings

from bot_init.models import Subscriber
from bot_init.schemas import Answer, SUBSCRIBER_ACTIONS


def get_tbot_instance() -> TeleBot:
    """Получаем экземпляр класса TeleBot для удобной работы с API"""
    return TeleBot(settings.TG_BOT.token)


def registration_subscriber(chat_id: int):
    """Логика сохранения подписчика"""
    subscriber, created = Subscriber.objects.get_or_create(tg_chat_id=chat_id)
    ...


def check_user_status_by_typing(chat_id: int):
    sub = get_subscriber_by_chat_id(chat_id)
    try:
        get_tbot_instance().send_chat_action(sub.tg_chat_id, 'typing')
        if not sub.is_active:
            sub.is_active = True
            sub.save(update_fields=['is_active'])
        return True
    except Exception as e:
        if ('bot was blocked by the user' in str(e) or 'user is deactivated' in str(e)) and sub.is_active:
            _subscriber_unsubscribed(sub.tg_chat_id)


def count_active_users():
    count = 0
    for sub in pbar(Subscriber.objects.all()):
        if check_user_status_by_typing(sub.tg_chat_id):
            count += 1
    return count


def create_action(subscriber: Subscriber, action: str):
    """Создаем запись в БД о подписке, отписке или реактивации бота пользователем"""
    SubscriberAction.objects.create(subscriber=subscriber, action=action)


def update_webhook(host=f'{settings.TG_BOT.webhook_host}/{settings.TG_BOT.token}'):
    """Обновляем webhook"""
    tbot = get_tbot_instance()
    tbot.remove_webhook()
    time.sleep(1)
    tbot.set_webhook(host)


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
