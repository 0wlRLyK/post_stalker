# Generated by Django 3.2 on 2021-04-30 20:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0027_auto_20210430_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='group_id',
            field=models.PositiveSmallIntegerField(default=1, null=True),
        ),
    ]
