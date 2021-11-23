from django.conf import settings
from django.db import models

from bot_init.schemas import SUBSCRIBER_ACTIONS


class Mailing(models.Model):
    """Класс объеденяющий сообщения для удобного удаления при некорректной рассылке."""

    pass


class AdminMessage(models.Model):
    """Административные сообщения."""

    title = models.CharField(max_length=128, verbose_name='Навзвание')
    text = models.TextField(verbose_name='Текст сообщения')
    key = models.CharField(max_length=128, verbose_name='Ключ, по которому сообщение вызывается в коде')

    def __str__(self):
        """Строковое представление."""
        return self.title

    class Meta:
        verbose_name = 'Админитративное сообщение'
        verbose_name_plural = 'Админитративные сообщения'


class Subscriber(models.Model):
    """Модель подписчика бота."""

    tg_chat_id = models.IntegerField(verbose_name="Идентификатор подписчика")
    is_active = models.BooleanField(default=True, verbose_name="Подписан ли польователь на бота")
    comment = models.TextField(null=True)
    ref_info = models.CharField(max_length=128, verbose_name="Реферальный код", null=True)

    def __str__(self):
        """Строковое представление."""
        return str(self.tg_chat_id)

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"


class Message(models.Model):
    """Модель для хранения сообщеинй."""

    date = models.DateTimeField(null=True, verbose_name="Дата отправки")
    from_user_id = models.IntegerField(verbose_name="Идентификатор отправителя")
    message_id = models.IntegerField(verbose_name="Идентификатор сообщения")
    chat_id = models.IntegerField(verbose_name="Идентификатор чата, в котором идет общение")
    text = models.TextField(null=True, verbose_name="Текст сообщения")
    json = models.TextField()
    mailing = models.ForeignKey(Mailing, related_name='messages', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        """Строковое представление."""
        if self.from_user_id == settings.TG_BOT.id:
            return f'⬆ {self.text}'
        else:
            return f'⬇ {self.text}'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class SubscriberAction(models.Model):
    """Действие подписчика.

    Нужно для того, чтобы удобно вести статистику, отслеживаем 3 варианта событий:
     - Пользователь подписался
     - Пользователь отписался
     - Пользователь реактивировался
    """

    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, verbose_name='Подписчик')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата/время')
    action = models.CharField(max_length=16, choices=SUBSCRIBER_ACTIONS, verbose_name='Действие')

    def __str__(self):
        """Строковое представление."""
        return f'{self.subscriber} {self.action}'

    class Meta:
        verbose_name = 'Действия пользователя'
        verbose_name_plural = 'Действия пользователей'
