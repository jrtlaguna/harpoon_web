# Generated by Django 3.2.9 on 2021-11-19 21:04

import authentication.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_create_custom_user_model"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", authentication.managers.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("ADMIN", "ADMIN"), ("GUEST", "GUEST")],
                default="GUEST",
                max_length=255,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
