# Generated by Django 3.2 on 2021-04-24 22:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0015_alter_moneytransaction_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(upload_to='users/awards/', verbose_name='Иконка награды')),
                ('name', models.CharField(max_length=75, verbose_name='Название награды')),
                ('description', models.TextField(verbose_name='Описание награды')),
            ],
            options={
                'verbose_name': 'Награда',
                'verbose_name_plural': 'Награды',
            },
        ),
        migrations.CreateModel(
            name='UserAward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_created=True)),
                ('message', models.TextField()),
                ('author',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='award_author',
                                   to=settings.AUTH_USER_MODEL)),
                ('award', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.award')),
                ('awarded',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='awarded_user',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Награда пользователя',
                'verbose_name_plural': 'Награды пользователя',
            },
        ),
    ]