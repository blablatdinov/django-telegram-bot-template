from datetime import datetime
from django.utils.timezone import make_aware
from bot_init.models import Message
import json


def save_message(msg):
    """ Сохранение сообщения от пользователя """
    date = make_aware(datetime.fromtimestamp(msg.date))
    from_user_id = msg.from_user.id
    message_id = msg.message_id
    chat_id = msg.chat.id
    text = msg.text
    try:
        json_str = msg.json
    except:
        json_str = str(msg)
    json_text = json.dumps(json_str, indent=2, ensure_ascii=False)
    Message.objects.create(date=date, from_user_id=from_user_id, message_id=message_id,
                           chat_id=chat_id, text=text, json=json_text)
