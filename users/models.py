import datetime
import re

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext as _
from userena.models import UserenaBaseProfile
from userena.models import UserenaSignup

from users.models_dir.equipment import Inventory
from users.online_users.models import OnlineUserActivity


def upload_to_item(instance, filename):
    return '/'.join(['Equipment', str(instance.item_type), filename])


class User(AbstractUser):
    GENDER_CHOICE = [
        (1, "Man"),
        (0, "Woman"),
    ]
    id = models.AutoField(primary_key=True)
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)
    ip = models.GenericIPAddressField(verbose_name="IP", null=True, blank=True)
    birthday = models.DateField(verbose_name="День рождения", null=True, blank=True)
    country = models.CharField(max_length=200, blank=True, null=True, verbose_name="Страна")
    state = models.CharField(max_length=200, blank=True, null=True, verbose_name="Город")
    signature = RichTextField(verbose_name="Подпись", blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Титул")
    gender = models.IntegerField(verbose_name="Пол", choices=GENDER_CHOICE, default=1)
    rank = models.IntegerField(default=0, blank=True)
    respect = models.SmallIntegerField(default=0, verbose_name="Репутация", blank=True)
    banreason = models.TextField(verbose_name="Причины блокировки", default="", blank=True, null=True)
    money = models.PositiveIntegerField(default=1000, verbose_name="Деньги форума")
    status = models.CharField(max_length=50, default="", verbose_name="Статус пользователя")
    ico_num = models.PositiveSmallIntegerField(default=1, verbose_name="Номер иконки")
    chat_color = models.CharField(max_length=10, verbose_name="Цвет", null=True, blank=True)

    equip = models.OneToOneField("Inventory", null=True, verbose_name="Снаряжение пользователя",
                                 on_delete=models.SET_NULL)
    group_id = models.PositiveSmallIntegerField(null=True, default=1)

    def valid_username(self):
        return bool(re.match(r'^[\w.@+-]+\Z', self.username))

    valid_username.allow_tags = True
    valid_username.short_description = "Validation"

    def last_seen(self):
        return cache.get('seen_%s' % self.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                    seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return "/media/post_st/ava/avatar.png"

    def get_group(self):
        if self.groups.count() > 0:
            return self.groups.first()
        else:
            self.groups.add(self.group_id)
            return self.groups.first()

    def get_fraction(self):
        if self.groups.count() > 0:
            return self.groups.first().gr_faction

    def get_rank(self):
        if self.rank < 50:
            return {
                "name": "Новичок",
                "url": "/static/post_stalker/users/ranks/rank1.gif"
            }
        elif self.rank < 100:
            return {
                "name": "Просвещённый",
                "url": "/static/post_stalker/users/ranks/rank2.gif"
            }
        elif self.rank < 100:
            return {
                "name": "Опытный",
                "url": "/static/post_stalker/users/ranks/rank3.gif"
            }
        elif self.rank < 250:
            return {
                "name": "Бывалый",
                "url": "/static/post_stalker/users/ranks/rank4.gif"
            }
        elif self.rank < 300:
            return {
                "name": "Профессионал",
                "url": "/static/post_stalker/users/ranks/rank5.gif"
            }
        elif self.rank < 500:
            return {
                "name": "Помеченный зоной",
                "url": "/static/post_stalker/users/ranks/rank6.gif"
            }
        elif self.rank < 700:
            return {
                "name": "Мастер",
                "url": "/static/post_stalker/users/ranks/rank7.gif"
            }
        elif self.rank < 800:
            return {
                "name": "Чёрный Сталкер",
                "url": "/static/post_stalker/users/ranks/rank8.gif"
            }
        elif self.rank < 1000:
            return {
                "name": "Призрак Зоны",
                "url": "/static/post_stalker/users/ranks/rank9.gif"
            }
        elif self.rank > 1000:
            return {
                "name": "Легенда Зоны",
                "url": "/static/post_stalker/users/ranks/rank10.gif"
            }

    def get_online(self):
        if OnlineUserActivity.check_user_online(user=self):
            return {
                "name": "",
                "url": "/static/post_stalker/users/v_zone.gif"
            }

        return {
            "name": "",
            "url": "/static/post_stalker/users/vne_zony.gif"
        }

    def get_gender(self):
        genders = ("Сталкерша", "Сталкер")
        return genders[self.gender]

    def get_age(self):
        today = datetime.date.today()
        if self.birthday:
            born = self.birthday
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return "Не указан"

    def get_awards_count(self):
        return self.awarded_user.count()

    def get_equipment(self):
        if self.equip_id:
            return self.equip
        else:
            inv = Inventory(id=self.id)
            inv.save()
            self.equip_id = inv.id
            super(User, self).save()
        return inv


class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile',
                                on_delete=models.CASCADE)
