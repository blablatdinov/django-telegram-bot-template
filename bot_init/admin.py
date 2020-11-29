from django.contrib import admin

from bot_init.models import Message, Subscriber

def tg_delete_messages(modeladmin, request, queryset):
    for message in queryset:
        message.tg_delete()
tg_delete_messages.short_description = "Удалить сообщения в телеграмм"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat_id", "text", "date")
    search_fields = ("text", "chat_id")
    actions = [tg_delete_messages]


admin.site.register(Subscriber)

