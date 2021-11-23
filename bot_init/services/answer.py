from loguru import logger

from bot_init.markup import get_default_keyboard
from bot_init.utils import get_tbot_instance

log = logger.bind(task="write_out_data")
app_log = logger.bind(task="app")
tbot = get_tbot_instance()


# TODO жирные методы
class Answer:
    """Класс ответа пользователю."""

    text = str
    keyboard = get_default_keyboard()
    chat_id: int

    def __init__(self, text, chat_id: int = None, keyboard=None, message_key=None):
        """Конструктор класса."""
        self.text = text
        if keyboard is not None:
            self.keyboard = keyboard
        if chat_id is not None:
            self.chat_id = chat_id
        self.message_key = message_key

    def send(self, chat_id: int = None):
        """Метод для отправки ответа."""
        from bot_init.utils import save_message
        if chat_id is None:
            chat_id = self.chat_id
        if chat_id is None:
            raise Exception("Не передан идентификатор чата")
        try:
            if self.keyboard:
                message = tbot.send_message(
                    chat_id=chat_id,
                    text=self.text,
                    reply_markup=self.keyboard,
                    parse_mode="HTML",
                )
                save_message(message, message_key=self.message_key)
                log.info(str(message))
                return
            message = tbot.send_message(chat_id=chat_id, text=self.text, parse_mode="HTML")
            log.info(str(message))
            save_message(message, message_key=self.message_key)
        except Exception as e:
            app_log.error(e)

    def edit(self, message_id: int, chat_id: int = None):
        """Метод для редактирования сообщения."""
        from bot_init.utils import save_message
        if chat_id is None:
            chat_id = self.chat_id
        if chat_id is None:
            raise Exception("Не передан идентификатор чата")
        try:
            if self.keyboard:
                message = tbot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=self.text,
                    reply_markup=self.keyboard,
                    parse_mode="HTML"
                )
                log.info(str(message))
                return
            message = tbot.send_message(chat_id=chat_id, text=self.text, parse_mode="HTML")
            log.info(str(message))
            save_message(message)
        except Exception as e:
            app_log.error(e)
