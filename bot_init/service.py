from bot_init.models import Subscriber


def registration_subscriber(chat_id: int):
    """Логика сохранения подписчика"""
    subscriber, created = Subscriber.objects.get_or_create(tg_chat_id=chat_id)
    ...
