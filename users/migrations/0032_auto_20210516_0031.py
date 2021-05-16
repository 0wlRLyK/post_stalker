# Generated by Django 3.2.2 on 2021-05-15 21:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0031_alter_applicationformembership_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationformembership',
            name='conformity',
        ),
        migrations.AlterField(
            model_name='applicationformembership',
            name='group',
            field=models.ForeignKey(limit_choices_to={'can_entry': True}, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL, to='users.fraction',
                                    verbose_name='Группа для вступления'),
        ),
        migrations.AlterField(
            model_name='applicationformembership',
            name='leader_message',
            field=models.TextField(blank=True, null=True, verbose_name='Ответ лидера группировки'),
        ),
        migrations.AlterField(
            model_name='applicationformembership',
            name='user_message',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='user',
            name='equip',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user',
                                       to='users.inventory', verbose_name='Снаряжение пользователя'),
        ),
    ]
