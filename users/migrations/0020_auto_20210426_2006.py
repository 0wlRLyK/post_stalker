# Generated by Django 3.2 on 2021-04-26 17:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0019_auto_20210426_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='Addon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название объекта')),
                ('description', models.TextField(verbose_name='Описание')),
                ('cost', models.PositiveSmallIntegerField(default=0, verbose_name='Стоимость')),
                ('icon', models.ImageField(upload_to='post_st/inventory/Equipment/addons/', verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Аддоны',
                'verbose_name_plural': 'Аддоны',
            },
        ),
        migrations.CreateModel(
            name='Ammo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название объекта')),
                ('description', models.TextField(verbose_name='Описание')),
                ('cost', models.PositiveSmallIntegerField(default=0, verbose_name='Стоимость')),
                ('icon', models.ImageField(upload_to='post_st/inventory/Equipment/ammo/', verbose_name='Иконка')),
                ('capacity', models.PositiveSmallIntegerField(default=0, verbose_name='Вместимость')),
            ],
            options={
                'verbose_name': 'Боерипасы 1 слота',
                'verbose_name_plural': 'Боерипасы 1 слота',
            },
        ),
        migrations.CreateModel(
            name='Grenade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название объекта')),
                ('description', models.TextField(verbose_name='Описание')),
                ('cost', models.PositiveSmallIntegerField(default=0, verbose_name='Стоимость')),
                ('icon', models.ImageField(upload_to='post_st/inventory/Equipment/grenades/', verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Гранаты',
                'verbose_name_plural': 'Гранаты',
            },
        ),
        migrations.CreateModel(
            name='Outfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название объекта')),
                ('description', models.TextField(verbose_name='Описание')),
                ('cost', models.PositiveSmallIntegerField(default=0, verbose_name='Стоимость')),
                ('icon', models.ImageField(upload_to='post_st/inventory/Equipment/', verbose_name='Иконка')),
                ('armor', models.PositiveSmallIntegerField(default=0, verbose_name='Броня')),
                ('protection', models.PositiveSmallIntegerField(default=0, verbose_name='Защита')),
            ],
            options={
                'verbose_name': 'Броня',
                'verbose_name_plural': 'Броня',
            },
        ),
        migrations.CreateModel(
            name='Pistol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название объекта')),
                ('description', models.TextField(verbose_name='Описание')),
                ('cost', models.PositiveSmallIntegerField(default=0, verbose_name='Стоимость')),
                ('icon', models.ImageField(upload_to='post_st/inventory/Guns/pistol/', verbose_name='Иконка')),
                ('capacity', models.PositiveSmallIntegerField(default=0, verbose_name='Вместимость')),
                ('damage', models.PositiveSmallIntegerField(default=0, verbose_name='Повреждение оружия')),
            ],
            options={
                'verbose_name': 'Оружие 2 слота',
                'verbose_name_plural': 'Оружие 2 слота',
            },
        ),
        migrations.CreateModel(
            name='PistolAmmo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название объекта')),
                ('description', models.TextField(verbose_name='Описание')),
                ('cost', models.PositiveSmallIntegerField(default=0, verbose_name='Стоимость')),
                (
                'icon', models.ImageField(upload_to='post_st/inventory/Equipment/pistol_ammo/', verbose_name='Иконка')),
                ('capacity', models.PositiveSmallIntegerField(default=0, verbose_name='Вместимость')),
            ],
            options={
                'verbose_name': 'Боерипасы 2 слота',
                'verbose_name_plural': 'Боерипасы 2 слота',
            },
        ),
        migrations.CreateModel(
            name='UpgradeOutfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название объекта')),
                ('description', models.TextField(verbose_name='Описание')),
                ('cost', models.PositiveSmallIntegerField(default=0, verbose_name='Стоимость')),
                ('icon',
                 models.ImageField(upload_to='post_st/inventory/Equipment/upgrades_equip/', verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Апгрейды брони',
                'verbose_name_plural': 'Апгрейды брони',
            },
        ),
        migrations.CreateModel(
            name='UpgradeWeapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название объекта')),
                ('description', models.TextField(verbose_name='Описание')),
                ('cost', models.PositiveSmallIntegerField(default=0, verbose_name='Стоимость')),
                ('icon',
                 models.ImageField(upload_to='post_st/inventory/Equipment/upgrades_weap/', verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Апгрейды оружия',
                'verbose_name_plural': 'Апгрейды оружия',
            },
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название объекта')),
                ('description', models.TextField(verbose_name='Описание')),
                ('cost', models.PositiveSmallIntegerField(default=0, verbose_name='Стоимость')),
                ('icon', models.ImageField(upload_to='post_st/inventory/Guns/', verbose_name='Иконка')),
                ('capacity', models.PositiveSmallIntegerField(default=0, verbose_name='Вместимость')),
                ('damage', models.PositiveSmallIntegerField(default=0, verbose_name='Повреждение оружия')),
            ],
            options={
                'verbose_name': 'Оружие 1 слота',
                'verbose_name_plural': 'Оружие 1 слота',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot1_condition', models.PositiveSmallIntegerField(default=100, verbose_name='Состояние 1 слота')),
                ('slot2_condition', models.PositiveSmallIntegerField(default=100, verbose_name='Состояние 2 слота')),
                ('slot3_condition', models.PositiveSmallIntegerField(default=100, verbose_name='Состояние 3 слота')),
                ('ammo_slot1_quantity',
                 models.PositiveSmallIntegerField(default=100, verbose_name='Кол-во боеприпасов 1 слота')),
                ('ammo_slot2_quantity',
                 models.PositiveSmallIntegerField(default=100, verbose_name='Кол-во боеприпасов 2 слота')),
                ('grenade_quantity',
                 models.PositiveSmallIntegerField(default=100, verbose_name='Кол-во боеприпасов 1 слота')),
                ('addon_slot1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                  related_name='wpn_addon', to='users.addon',
                                                  verbose_name='Аддон 1 слота')),
                ('addon_slot2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                  related_name='pst_addon', to='users.addon',
                                                  verbose_name='Аддон 2 слота')),
                ('ammo_slot1',
                 models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.ammo',
                                   verbose_name='Боеприпасы 1 слота')),
                ('ammo_slot2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                 to='users.pistolammo', verbose_name='Боеприпасы 2 слота')),
                ('grenade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                              to='users.grenade', verbose_name='Гранаты')),
                ('slot1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                            to='users.weapon', verbose_name='Слот 1')),
                ('slot2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                            to='users.pistol', verbose_name='Слот 2')),
                ('slot3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                            to='users.outfit', verbose_name='Слот 3')),
                ('upgrades_slot1',
                 models.ManyToManyField(blank=True, related_name='slot1_upgr', to='users.UpgradeWeapon',
                                        verbose_name='Апгрейды 1 слота')),
                ('upgrades_slot2',
                 models.ManyToManyField(blank=True, related_name='slot2_upgr', to='users.UpgradeWeapon',
                                        verbose_name='Апгрейды 2 слота')),
                ('upgrades_slot3',
                 models.ManyToManyField(blank=True, related_name='slot3_upgr', to='users.UpgradeOutfit',
                                        verbose_name='Апгрейды 3 слота')),
            ],
            options={
                'verbose_name': 'Снаряжение',
                'verbose_name_plural': 'Снаряжение',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='equip',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.inventory',
                                       verbose_name='Снаряжение пользователя'),
        ),
    ]
