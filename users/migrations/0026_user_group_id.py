# Generated by Django 3.2 on 2021-04-30 19:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0025_auto_20210429_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='group_id',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]