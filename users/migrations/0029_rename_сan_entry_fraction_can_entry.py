# Generated by Django 3.2 on 2021-05-08 21:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0028_alter_user_group_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fraction',
            old_name='сan_entry',
            new_name='can_entry',
        ),
    ]
