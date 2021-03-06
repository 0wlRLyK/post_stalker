# Generated by Django 3.2 on 2021-04-20 18:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0005_auto_20210418_0024'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reputation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=0, verbose_name='Значение')),
                ('add_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время и дата добавления')),
                ('subject', models.CharField(max_length=50, verbose_name='Причина изменения репутации')),
                ('message', models.TextField(verbose_name='Текст сообщения')),
                ('from_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='from_rep',
                                   to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
                ('to_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_rep',
                                   to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
            ],
            options={
                'verbose_name': 'Ед. репутации',
                'verbose_name_plural': 'Репутация',
            },
        ),
    ]
