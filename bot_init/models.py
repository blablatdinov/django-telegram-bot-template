from django.db import models


class Subscriber(models.Model):
    """ Модель подписчика бота """
    tg_chat_id = models.IntegerField(verbose_name="Идентификатор подписчика")
    is_active = models.BooleanField(default=True, verbose_name="Подписан ли польователь на бота")
    comment = models.TextField(null=True)

    def __str__(self):
        str(self.tg_chat_id)

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"


class Message(models.Model):
    """ Модель для хранения сообщеинй """
    date = models.DateTimeField(null=True, verbose_name="Дата отправки")
    from_user_id = models.IntegerField(verbose_name="Идентификатор отправителя")
    message_id = models.IntegerField(verbose_name="Идентификатор сообщения")
    chat_id = models.IntegerField(verbose_name="Идентификатор чата, в котором идет общение")
    text = models.TextField(null=True, verbose_name="Текст сообщения")
    json = models.TextField()

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
