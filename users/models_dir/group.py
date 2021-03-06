from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models

from users.models import User
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

    def get_group_name(self):
        return self.group.name

    def get_users_count(self):
        return User.objects.filter(groups__id=self.group_id).count()

    def __str__(self):
        return "{}".format(self.group.name)


class ApplicationForMembership(models.Model):
    user = models.ForeignKey(User, verbose_name="Автор заявления", null=True, on_delete=models.SET_NULL,
                             related_name="application_user")
    group = models.ForeignKey(Fraction, verbose_name="Группа для вступления", null=True,
                              on_delete=models.SET_NULL, limit_choices_to={"can_entry": True})
    leader = models.ForeignKey(User, verbose_name="Лидер группировки", blank=True, null=True, on_delete=models.SET_NULL,
                               related_name="application_leader")
    add_datetime = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Время и дата добавления")
    user_message = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    leader_message = models.TextField(blank=True, null=True, verbose_name="Ответ лидера группировки")
    decision = models.BooleanField(default=False, verbose_name="Разрешение/Отказ на вступление")
    archived = models.BooleanField(default=False, verbose_name="Архивное заявление",
                                   help_text="Данное заявление уже было рассмотрено лидером группировки")
    banished = models.BooleanField(default=False, verbose_name="Изгнан")

    def get_app_status(self):
        if self.archived and not self.decision and not self.banished:
            return "refused"
        elif self.archived and self.decision and not self.banished:
            return "accepted"
        elif self.archived and self.banished:
            return "banished"
        else:
            return "default"

    def get_leader_msg(self):
        if self.leader_message:
            return self.leader_message
        elif self.archived and not self.decision and not self.banished:
            return "Отказано"
        elif self.archived and self.decision and not self.banished:
            return "Принят"
        elif self.archived and self.banished:
            return "Изгнан"
        else:
            return "(Заяка в процессе рассмотрения)"

    class Meta:
        verbose_name = "Заявка на вступление в группировку"
        verbose_name_plural = "Заявки на вступление в группировку"
