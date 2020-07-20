"""
Модуль, содержащий классы и функции для создания клавиатур.

"""
from telebot import types


class InlineKeyboard:
    """ Класс создающий клавиатуру над строкой ввода сообщений """

    def get_lines(self, buttons):
        """ Метод для получения строк """
        for line in buttons:
            buttons_line = []
            for button_text in line:
                button = self.get_buttons(button_text)
                buttons_line.append(button)
            yield buttons_line

    def get_buttons(self, button_text):
        """ Метод для получения кнопок """
        if isinstance(button_text, str):
            button = types.InlineKeyboardButton(text=button_text, callback_data=button_text)
        if isinstance(button_text, tuple):
            button = types.InlineKeyboardButton(text=button_text[0], callback_data=button_text[1])
        return button

    def __init__(self, buttons):
        """
        example = (
            (('button1', 'value1'), ('button2', 'value2')),
            (('button3', 'value3'),)
        )
        Уровни вложенности:
            1. Все кнопки
            2. Строки
            3. Кнопки и их значения
        """
        self.keyboard = types.InlineKeyboardMarkup()
        lines = self.get_lines(buttons)
        for line in lines:
            self.keyboard.add(*line)


class Keyboard:
    """ Класс создающий клавиатуру под строкой ввода сообщений """

    def __init__(self, buttons):
        """
        example = (
            ('button1', 'button2'),
            ('button3',)
        )
        """
        self.keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        lines = self.get_lines(buttons)
        for line in lines:
            self.keyboard.add(*line)

    def get_lines(self, buttons):
        """ Метод для получения строк """
        for line in buttons:
            buttons_line = []
            for button_text in line:
                button = self.get_buttons(button_text)
                buttons_line.append(button)
            yield buttons_line

    def get_buttons(self, button_text):
        """ Метод для получения кнопок """
        button = types.KeyboardButton(button_text)
        return button
