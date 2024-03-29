# Generated by Django 3.2.9 on 2022-01-13 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("charter", "0023_charter_principal_migration"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="guestdetail",
            name="charter",
        ),
        migrations.RemoveField(
            model_name="guestdetail",
            name="is_principal",
        ),
        migrations.AlterField(
            model_name="guestdetail",
            name="charters",
            field=models.ManyToManyField(
                related_name="guests", to="charter.Charter", verbose_name="Trips"
            ),
        ),
    ]
