# Generated by Django 3.2 on 2021-04-26 21:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0021_auto_20210426_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addon',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='ammo',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='grenade',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='ammo_slot1_quantity',
            field=models.PositiveSmallIntegerField(default=0, null=True, verbose_name='Кол-во боеприпасов 1 слота'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='ammo_slot2_quantity',
            field=models.PositiveSmallIntegerField(default=0, null=True, verbose_name='Кол-во боеприпасов 2 слота'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='grenade_quantity',
            field=models.PositiveSmallIntegerField(default=0, null=True, verbose_name='Кол-во боеприпасов 1 слота'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='slot1_condition',
            field=models.PositiveSmallIntegerField(default=100, null=True, verbose_name='Состояние 1 слота'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='slot2_condition',
            field=models.PositiveSmallIntegerField(default=100, null=True, verbose_name='Состояние 2 слота'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='slot3_condition',
            field=models.PositiveSmallIntegerField(default=100, null=True, verbose_name='Состояние 3 слота'),
        ),
        migrations.AlterField(
            model_name='outfit',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='pistol',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='pistolammo',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='upgradeoutfit',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='upgradeweapon',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='weapon',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]