# Generated by Django 3.2.2 on 2021-05-14 17:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0029_rename_сan_entry_fraction_can_entry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.IntegerField(choices=[(1, 'Сталкер'), (0, 'Сталкерша')], default=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='my_profile',
                                       to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.CreateModel(
            name='ApplicationForMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_message', models.TextField(blank=True, verbose_name='Сообщение пользователя')),
                ('leader_message', models.TextField(blank=True, verbose_name='Ответ лидера группировки')),
                ('conformity', models.BooleanField(default=False, verbose_name='Соответствие условиям')),
                ('decision', models.BooleanField(default=False, verbose_name='Разрешение/Отказ на вступление')),
                ('archived', models.BooleanField(default=False,
                                                 help_text='Данное заявление уже было рассмотрено лидером группировки',
                                                 verbose_name='Архивное заявление')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group',
                                            verbose_name='Группа в которую хочет вступить')),
                ('user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL,
                                   verbose_name='Автор заявления')),
            ],
        ),
    ]