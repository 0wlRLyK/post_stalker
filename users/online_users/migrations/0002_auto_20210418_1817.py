# Generated by Django 3.2 on 2021-04-18 15:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('online_users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='onlineuseractivity',
            options={'verbose_name': 'User Activity', 'verbose_name_plural': 'User Activity'},
        ),
        migrations.AlterField(
            model_name='onlineuseractivity',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
