# Generated by Django 3.2 on 2021-04-26 14:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0018_alter_useraward_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='addon1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='addon2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='addon3',
        ),
        migrations.RemoveField(
            model_name='user',
            name='ammo1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='ammo2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='slot1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='slot2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='slot3',
        ),
        migrations.RemoveField(
            model_name='user',
            name='upgrade1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='upgrade2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='upgrade3',
        ),
        migrations.DeleteModel(
            name='EquipItem',
        ),
        migrations.DeleteModel(
            name='InventoryItem',
        ),
    ]
