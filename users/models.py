import datetime
import re

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres import fields
from django.core.cache import cache
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext as _
from userena.models import UserenaBaseProfile

from users.online_users.models import OnlineUserActivity
from utils.models import SingletonModel


class UserSettings(SingletonModel):
    respect_pagination = models.PositiveSmallIntegerField(default=15,
                                                          verbose_name="Колличество записей изменения репутации на странице")
    transact_pagination = models.PositiveSmallIntegerField(default=15,
                                                           verbose_name="Колличетсво транзакций на странице")
    ico_range_numbers = fields.IntegerRangeField(verbose_name="Диапазон пользовательских иконок чата", null=True)

    nik_price = models.PositiveSmallIntegerField(default=500, verbose_name="Цена смена ника")
    chat_ico_price = models.PositiveSmallIntegerField(default=500, verbose_name="Цена смены иконки чата")
    chat_color_price = models.PositiveSmallIntegerField(default=300, verbose_name="Цена смены цвета чата")

    def __str__(self):
        return "Настройки"

    class Meta:
        verbose_name = "!Настройки модуля пользователей"
        verbose_name_plural = "!Настройки модуля пользователей"


def upload_to_item(instance, filename):
    return '/'.join(['Equipment', str(instance.item_type), filename])


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
    status = models.CharField(max_length=50, default="", verbose_name="Статус пользователя")
    ico_num = models.PositiveSmallIntegerField(default=1, verbose_name="Номер иконки")
    chat_color = models.CharField(max_length=10, verbose_name="Цвет", null=True, blank=True)

    equip = models.OneToOneField("Inventory", null=True, verbose_name="Снаряжение пользователя",
                                 on_delete=models.SET_NULL)

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
    author = models.ForeignKey(User, related_name="award_author", null=True, on_delete=models.SET_NULL)
    awarded = models.ForeignKey(User, related_name="awarded_user", null=True, on_delete=models.SET_NULL)
    create_datetime = models.DateTimeField(auto_now_add=True)
    message = models.TextField(verbose_name="Сообщение", blank=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Награда пользователя"
        verbose_name_plural = "Награды пользователя"


class EquipItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name="Название объекта")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    cost = models.PositiveSmallIntegerField(default=0, verbose_name="Стоимость", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Weapon(EquipItem):
    icon = models.ImageField(upload_to="post_st/inventory/Guns/", verbose_name="Иконка")
    capacity = models.PositiveSmallIntegerField(default=0, verbose_name="Вместимость", blank=True)
    damage = models.PositiveSmallIntegerField(default=0, verbose_name="Повреждение оружия", blank=True)

    def icon_admin(self):
        return format_html('<center><img href="{0}" src="{0}" style="transform: rotate(90deg);padding: 0;margin: '
                           '0; height: 100px"/></center>'.format(self.icon.url))

    icon_admin.allow_tags = True
    icon_admin.short_description = 'Иконка'

    class Meta:
        verbose_name_plural = verbose_name = "Оружие 1 слота"


class Pistol(EquipItem):
    icon = models.ImageField(upload_to="post_st/inventory/Guns/pistol/", verbose_name="Иконка")
    capacity = models.PositiveSmallIntegerField(default=0, verbose_name="Вместимость", blank=True)
    damage = models.PositiveSmallIntegerField(default=0, verbose_name="Повреждение оружия", blank=True)

    def icon_admin(self):
        return format_html('<center><img href="{0}" src="{0}" style="transform: rotate(90deg);padding: 0;margin: '
                           '0; height: 100px"/></center>'.format(self.icon.url))

    icon_admin.allow_tags = True
    icon_admin.short_description = 'Иконка'

    class Meta:
        verbose_name_plural = verbose_name = "Оружие 2 слота"


class Outfit(EquipItem):
    icon = models.ImageField(upload_to="post_st/inventory/Equipment/", verbose_name="Иконка")
    armor = models.PositiveSmallIntegerField(default=0, verbose_name="Броня", blank=True)
    protection = models.PositiveSmallIntegerField(default=0, verbose_name="Защита", blank=True)

    def icon_admin(self):
        return format_html('<center><img href="{0}" src="{0}" /></center>'.format(self.icon.url))

    icon_admin.allow_tags = True
    icon_admin.short_description = 'Иконка'

    class Meta:
        verbose_name_plural = verbose_name = "Броня"


class Ammo(EquipItem):
    icon = models.ImageField(upload_to="post_st/inventory/Equipment/ammo/", verbose_name="Иконка", blank=True)
    capacity = models.PositiveSmallIntegerField(default=0, verbose_name="Вместимость", blank=True)

    def icon_admin(self):
        return format_html('<center><img href="{0}" src="{0}" /></center>'.format(self.icon.url))

    icon_admin.allow_tags = True
    icon_admin.short_description = 'Иконка'

    class Meta:
        verbose_name_plural = verbose_name = "Боерипасы 1 слота"


class PistolAmmo(EquipItem):
    icon = models.ImageField(upload_to="post_st/inventory/Equipment/pistol_ammo/", verbose_name="Иконка")
    capacity = models.PositiveSmallIntegerField(default=0, verbose_name="Вместимость", blank=True)

    def icon_admin(self):
        return format_html('<center><img href="{0}" src="{0}" /></center>'.format(self.icon.url))

    icon_admin.allow_tags = True
    icon_admin.short_description = 'Иконка'

    class Meta:
        verbose_name_plural = verbose_name = "Боерипасы 2 слота"


class Grenade(EquipItem):
    icon = models.ImageField(upload_to="post_st/inventory/Equipment/grenades/", verbose_name="Иконка", blank=True)

    def icon_admin(self):
        return format_html('<center><img href="{0}" src="{0}" /></center>'.format(self.icon.url))

    icon_admin.allow_tags = True
    icon_admin.short_description = 'Иконка'

    class Meta:
        verbose_name_plural = verbose_name = "Гранаты"


class Addon(EquipItem):
    icon = models.ImageField(upload_to="post_st/inventory/Equipment/addons/", verbose_name="Иконка", blank=True)

    def icon_admin(self):
        return format_html('<center><img href="{0}" src="{0}" /></center>'.format(self.icon.url))

    icon_admin.allow_tags = True
    icon_admin.short_description = 'Иконка'

    class Meta:
        verbose_name_plural = verbose_name = "Аддоны"


class UpgradeWeapon(EquipItem):
    icon = models.ImageField(upload_to="post_st/inventory/Equipment/upgrades_weap/", verbose_name="Иконка", blank=True)

    def icon_admin(self):
        return format_html('<center><img href="{0}" src="{0}" /></center>'.format(self.icon.url))

    icon_admin.allow_tags = True
    icon_admin.short_description = 'Иконка'

    class Meta:
        verbose_name_plural = verbose_name = "Апгрейды оружия"


class UpgradeOutfit(EquipItem):
    icon = models.ImageField(upload_to="post_st/inventory/Equipment/upgrades_equip/", verbose_name="Иконка", blank=True)

    def icon_admin(self):
        return format_html('<center><img href="{0}" src="{0}" /></center>'.format(self.icon.url))

    icon_admin.allow_tags = True
    icon_admin.short_description = 'Иконка'

    class Meta:
        verbose_name_plural = verbose_name = "Апгрейды брони"


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    slot1 = models.ForeignKey(Weapon, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Слот 1")
    slot1_condition = models.PositiveSmallIntegerField(default=100, null=True, verbose_name="Состояние 1 слота")
    slot2 = models.ForeignKey(Pistol, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Слот 2")
    slot2_condition = models.PositiveSmallIntegerField(default=100, null=True, verbose_name="Состояние 2 слота")
    slot3 = models.ForeignKey(Outfit, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Слот 3")
    slot3_condition = models.PositiveSmallIntegerField(default=100, null=True, verbose_name="Состояние 3 слота")
    ammo_slot1 = models.ForeignKey(Ammo, on_delete=models.SET_NULL, blank=True, null=True,
                                   verbose_name="Боеприпасы 1 слота")
    ammo_slot1_quantity = models.PositiveSmallIntegerField(default=0, null=True,
                                                           verbose_name="Кол-во боеприпасов 1 слота")
    ammo_slot2 = models.ForeignKey(PistolAmmo, on_delete=models.SET_NULL, blank=True, null=True,
                                   verbose_name="Боеприпасы 2 слота")
    ammo_slot2_quantity = models.PositiveSmallIntegerField(default=0, null=True,
                                                           verbose_name="Кол-во боеприпасов 2 слота")
    grenade = models.ForeignKey(Grenade, on_delete=models.SET_NULL, blank=True, null=True,
                                verbose_name="Гранаты")
    grenade_quantity = models.PositiveSmallIntegerField(default=0, null=True, verbose_name="Кол-во боеприпасов 1 слота")
    addon_slot1 = models.ForeignKey(Addon, on_delete=models.SET_NULL, blank=True, null=True, related_name="wpn_addon",
                                    verbose_name="Аддон 1 слота")
    addon_slot2 = models.ForeignKey(Addon, on_delete=models.SET_NULL, blank=True, null=True, related_name="pst_addon",
                                    verbose_name="Аддон 2 слота")
    upgrades_slot1 = models.ManyToManyField(UpgradeWeapon, verbose_name="Апгрейды 1 слота", blank=True,
                                            related_name="slot1_upgr")
    upgrades_slot2 = models.ManyToManyField(UpgradeWeapon, verbose_name="Апгрейды 2 слота", blank=True,
                                            related_name="slot2_upgr")
    upgrades_slot3 = models.ManyToManyField(UpgradeOutfit, verbose_name="Апгрейды 3 слота", blank=True,
                                            related_name="slot3_upgr")

    @staticmethod
    def condition_color(percents):
        if percents >= 75:
            return "st_green"
        elif (percents < 75) and (percents >= 50):
            return "st_yellow"
        elif (percents < 50) and (percents >= 25):
            return "st_orange"
        elif (percents < 25) and (percents >= 0):
            return "st_red"

    def get_sl1c_class(self):
        return self.condition_color(self.slot1_condition)

    def get_sl2c_class(self):
        return self.condition_color(self.slot2_condition)

    def get_sl3c_class(self):
        return self.condition_color(self.slot3_condition)

    class Meta:
        verbose_name = verbose_name_plural = "Снаряжение"
