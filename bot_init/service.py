def registration_subscriber(message):
    """ Логика сохранения подписчика """
    subscriber, created = Subscriber.objects.get_or_create(tg_chat_id=message.chat.id)
    ...
