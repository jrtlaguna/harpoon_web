# Generated by Django 3.2.9 on 2022-02-11 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("charter", "0036_remove_charter_number_of_guests"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dietservicessizespreferences",
            name="favorite_flowers",
        ),
    ]
