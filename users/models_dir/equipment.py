from django.db import models
from django.utils.html import format_html


# Equipment

class EquipItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name="Название объекта")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    cost = models.PositiveSmallIntegerField(default=0, verbose_name="Стоимость", blank=True)

    def __str__(self):
        return self.name

    def get_sell_cost(self):
        return self.cost // 2

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

    def get_username(self):
        if self.user:
            return self.user.username
        return None

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = verbose_name_plural = "Снаряжение"
