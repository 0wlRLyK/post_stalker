# Generated by Django 3.2.2 on 2021-05-12 20:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('online_users', '0002_auto_20210418_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineuseractivity',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]