# Generated by Django 3.2.9 on 2021-12-28 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("charter", "0013_auto_20211221_1319"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Guest",
            new_name="GuestDetail",
        ),
        migrations.AlterModelOptions(
            name="guestdetail",
            options={"verbose_name_plural": "Guest Details"},
        ),
    ]
