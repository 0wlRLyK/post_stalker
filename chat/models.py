from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.html import format_html


class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_username):  # get_or_create
        username = user.username
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            if user != user2:
                obj = self.model(
                    first=user,
                    second=user2
                )
                obj.save()
                return obj, True
            return None, False


class Thread(models.Model):
    first = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_first')
    second = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    @property
    def room_group_name(self):
        return f'dialog_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False


class Chat(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название чата")
    slug = models.SlugField(verbose_name="Slug")
    in_chats = models.BooleanField(default=False, verbose_name="Выводить в списке чатов")
    roleplay = models.BooleanField(verbose_name="Чат ролевой игры", default=False)
    preview = models.ImageField(default="roleplay/default/campfire.jpg", upload_to="roleplay/campfire",
                                verbose_name="Превью")

    def icon_admin(self):
        return format_html(
            '<center><img href="{0}" src="{0}" height="100" width="100" style="border-radius: 100%" /></center>'.format(
                self.preview.url))

    icon_admin.allow_tags = True
    icon_admin.short_description = 'Иконка'

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"


class AbstractMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='sender', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class DialogMessage(AbstractMessage):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)


class ChatMessage(AbstractMessage):
    thread = models.ForeignKey(Chat, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-timestamp"]
