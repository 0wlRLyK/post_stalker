from django.conf import settings
from django.db import models
from django.utils.html import format_html


# Reputation, Money, Awards

class Reputation(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="Получатель",
                                  related_name="from_rep",
                                  null=True)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="Отправитель",
                                related_name="to_rep",
                                null=True)
    value = models.SmallIntegerField(default=0, verbose_name="Значение")
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Время и дата добавления")
    subject = models.TextField(verbose_name="Причина изменения репутации", null=True)
    message = models.TextField(verbose_name="Текст сообщения", blank=True, null=True)

    def get_level(self):
        if self.value < 0:
            return {"ico": "minus.svg",
                    "sign": "-",
                    "text": "Уровень понижен"}
        elif self.value > 0:
            return {"ico": "plus.svg",
                    "sign": "+",
                    "text": "Уровень повышен"}
        return {"ico": "bulb.svg",
                "sign": "",
                "text": "Уровень репутации не изменен"}

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Ед. репутации"
        verbose_name_plural = "Репутация"


class MoneyTransaction(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="Получатель",
                                  related_name="from_transaction",
                                  null=True)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="Отправитель",
                                related_name="to_transaction",
                                null=True)
    value = models.IntegerField(default=0, verbose_name="Значение")
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Время и дата добавления")
    message = models.TextField(verbose_name="Комментарий перевода", blank=True, null=True)

    def __str__(self):
        return f'{self.from_user.username}>>{self.to_user.username}:{self.value} - {self.message}'

    def get_range(self):
        if self.value > 0:
            return {"sign": "+",
                    "class": "positive"}
        elif self.value < 0:
            return {"sign": "",
                    "class": "negative"}
        return {"sign": "",
                "class": "null"}

    class Meta:
        verbose_name = "Денежный перевод"
        verbose_name_plural = "Денежные переводы"

    class SingletonModel(models.Model):
        class Meta:
            abstract = True

        def save(self, *args, **kwargs):
            self.__class__.objects.exclude(id=self.id).delete()
            super().save(*args, **kwargs)

        @classmethod
        def load(cls):
            try:
                return cls.objects.get()
            except cls.DoesNotExist:
                return cls()


class Award(models.Model):
    icon = models.ImageField(upload_to="users/awards/", verbose_name="Иконка награды")
    name = models.CharField(max_length=75, verbose_name="Название награды")
    description = models.TextField(verbose_name="Описание награды", blank=True)

    def icon_admin(self):
        return format_html('<center><img href="{0}" src="{0}" /></center>'.format(self.icon.url))

    icon_admin.allow_tags = True
    icon_admin.short_description = 'Иконка'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Награда"
        verbose_name_plural = "Награды"


class UserAward(models.Model):
    id = models.AutoField(primary_key=True)
    award = models.ForeignKey(Award, null=True, on_delete=models.SET_NULL, verbose_name="Награда")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="award_author", null=True,
                               on_delete=models.SET_NULL)
    awarded = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="awarded_user", null=True,
                                on_delete=models.SET_NULL)
    create_datetime = models.DateTimeField(auto_now_add=True)
    message = models.TextField(verbose_name="Сообщение", blank=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Награда пользователя"
        verbose_name_plural = "Награды пользователя"
