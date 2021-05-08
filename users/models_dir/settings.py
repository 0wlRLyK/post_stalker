from django.contrib.postgres import fields
from django.db import models

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
