# Generated by Django 3.2.9 on 2022-08-05 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("guests", "0001_create_guest_profile"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="guestprofile",
            options={
                "verbose_name": "Guest Profile",
                "verbose_name_plural": "Guest Profiles",
            },
        ),
    ]
