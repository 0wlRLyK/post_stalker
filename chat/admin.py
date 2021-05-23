from django.contrib import admin

from .models import Thread, DialogMessage, Chat, ChatMessage


class DialogMessageInline(admin.TabularInline):
    model = DialogMessage


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    inlines = [DialogMessageInline]

    class Meta:
        model = Thread


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage


@admin.register(Chat)
class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessageInline]
    list_display = ["name", "slug", "in_chats", "roleplay", "icon_admin"]

    class Meta:
        model = Chat
