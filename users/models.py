from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


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
