import datetime

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext as _
from userena.models import UserenaBaseProfile

from users.online_users.models import OnlineUserActivity


def upload_to_item(instance, filename):
    return '/'.join(['Equipment', str(instance.item_type), filename])


class InventoryItem(models.Model):
    WEAPON = 'WPN'
    GUN = 'GUN'
    ARMOR = 'ARM'
    AMMUNITION_1 = 'AMMO1'
    AMMUNITION_2 = 'AMMO2'
    GRENADE = 'GRND'
    ADDON = 'ADD'
    WEAPON_UP = 'WUP'
    GUN_UP = 'GUP'
    ARMOR_UP = 'AUP'
    INV_TYPES = [
        (WEAPON, 'Оружие 1слот'),
        (GUN, 'Оружие 2слот'),
        (ARMOR, 'Броня'),
        (AMMUNITION_1, 'Аммуниция 1слот'),
        (AMMUNITION_2, 'Аммуниция 2слот'),
        (GRENADE, 'Гранаты'),
        (ADDON, 'Аддоны'),
        (WEAPON_UP, 'Апгрейды 1слот'),
        (GUN_UP, 'Апгрейды 2слот'),
        (ARMOR_UP, 'Апгрейды брони'),
    ]
    name = models.CharField(max_length=200, verbose_name="Название")
    description = RichTextField(verbose_name="Описание", blank=True)
    image = models.ImageField(verbose_name="Иконка", upload_to=upload_to_item)
    item_type = models.CharField(max_length=5, verbose_name="Тип снаряжения", choices=INV_TYPES)

    def __str__(self):
        return self.name


class EquipItem(models.Model):
    item = models.ForeignKey(InventoryItem, verbose_name="Объект", on_delete=models.SET_NULL, null=True)
    condition = models.SmallIntegerField(default=100, verbose_name="Состояние")
    quantity = models.SmallIntegerField(default=0, verbose_name="Колличество")
    capacity = models.SmallIntegerField(default=0, verbose_name="Заряд")


class User(AbstractUser):
    GENDER_CHOICE = [
        (1, "Man"),
        (0, "Woman"),
    ]
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

    slot1 = models.ForeignKey(EquipItem, blank=True, null=True, on_delete=models.SET_NULL, related_name="uslot1")
    slot2 = models.ForeignKey(EquipItem, blank=True, null=True, on_delete=models.SET_NULL, related_name="uslot2")
    slot3 = models.ForeignKey(EquipItem, blank=True, null=True, on_delete=models.SET_NULL, related_name="uslot3")
    addon1 = models.ForeignKey(EquipItem, blank=True, null=True, on_delete=models.SET_NULL, related_name="uaddon1")
    addon2 = models.ForeignKey(EquipItem, blank=True, null=True, on_delete=models.SET_NULL, related_name="uaddon2")
    addon3 = models.ForeignKey(EquipItem, blank=True, null=True, on_delete=models.SET_NULL, related_name="uaddon3")
    ammo1 = models.ForeignKey(InventoryItem, blank=True, null=True, on_delete=models.SET_NULL, related_name="uammo1")
    ammo2 = models.ForeignKey(InventoryItem, blank=True, null=True, on_delete=models.SET_NULL, related_name="uammo2")
    upgrade1 = models.ManyToManyField(InventoryItem, blank=True, related_name="user_upgr1")
    upgrade2 = models.ManyToManyField(InventoryItem, blank=True, related_name="user_upgr2")
    upgrade3 = models.ManyToManyField(InventoryItem, blank=True, related_name="user_upgr3")
    is_online = models.BooleanField(default=False)

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

    def get_group_icon(self):
        if self.is_authenticated:
            group = self.groups.first()
            if group:
                return "/static/post_stalker/users/groups/{}.gif".format(group.id)
            else:
                return "/static/post_stalker/users/groups/1.gif"
        return "/static/post_stalker/users/groups/0.gif"

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
        born = self.birthday
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile',
                                on_delete=models.CASCADE)


class Reputation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Получатель", related_name="from_rep",
                                  null=True)
    to_user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Отправитель", related_name="to_rep",
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
    from_user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Получатель",
                                  related_name="from_transaction",
                                  null=True)
    to_user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Отправитель",
                                related_name="to_transaction",
                                null=True)
    value = models.PositiveIntegerField(default=0, verbose_name="Значение")
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Время и дата добавления")
    message = models.TextField(verbose_name="Комментарий перевода", blank=True, null=True)

    def __str__(self):
        return f'{self.from_user.username}>>{self.to_user.username}:{self.value} - {self.message}'

    def get_range(self):
        if self.value > 0:
            return {"sign": "+",
                    "class": "positive"}
        elif self.value < 0:
            return {"sign": "-",
                    "class": "negative"}
        return {"sign": "",
                "class": "null"}

    class Meta:
        verbose_name = "Денежный перевод"
        verbose_name_plural = "Денежные переводы"
