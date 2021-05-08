from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models

from users.models_dir import equipment


class Fraction(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.OneToOneField(Group, unique=True, related_name="gr_faction", null=True, on_delete=models.SET_NULL)
    description = models.TextField(verbose_name="Описание группировки", blank=True)
    leader = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Лидер", blank=True, null=True,
                                  related_name="faction_lead",
                                  on_delete=models.SET_NULL)
    deputy_leader = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Заместитель лидера", blank=True,
                                         null=True,
                                         related_name="faction_zam", on_delete=models.SET_NULL)
    icon = models.ImageField(upload_to="users/factions/", verbose_name="Маленькая иконка группировки",
                             help_text="Отображается в профиле пользователя", null=True)
    big_icon = models.ImageField(upload_to="users/factions/big/", verbose_name="Большая иконка группировки",
                                 help_text="Отображается в списке группировок", null=True)
    power = models.PositiveSmallIntegerField(verbose_name="Силы группировки", default=0, help_text="От 0 до 31")

    rng_weapons = models.ManyToManyField(equipment.Weapon, related_name="faction_wpn",
                                         verbose_name="Ассортимент оружия",
                                         help_text="1 слот", blank=True)
    rng_pistols = models.ManyToManyField(equipment.Pistol, related_name="faction_pst",
                                         verbose_name="Ассортимент оружия",
                                         help_text="2 слот", blank=True)
    rng_outfits = models.ManyToManyField(equipment.Outfit, related_name="faction_bron",
                                         verbose_name="Ассортимент брони",
                                         blank=True)
    rng_ammo1 = models.ManyToManyField(equipment.Ammo, related_name="faction_w_ammo",
                                       verbose_name="Ассортимент боеприпасов",
                                       help_text="1 слот", blank=True)
    rng_ammo2 = models.ManyToManyField(equipment.PistolAmmo, related_name="faction_p_ammo",
                                       verbose_name="Ассортимент боеприпасов",
                                       help_text="2 слот", blank=True)

    # ER - Entry Requirements (Требования к вступлению)
    er_respect = models.PositiveSmallIntegerField(default=10, verbose_name="Репутация для вступления")
    er_messages = models.PositiveSmallIntegerField(default=10, verbose_name="Сообщений для вступления")
    er_no_bans = models.BooleanField(default=True, verbose_name="Отстутствие замечаний для вступления")
    er_text = models.TextField(default="", verbose_name="Дополнительные пожелания", blank=True)

    show_in_list = models.BooleanField(default=True, verbose_name="Отображать в списке групп")
    can_entry = models.BooleanField(default=True, verbose_name="Возможность вступления")

    def __str__(self):
        return "{}".format(self.group.name)
