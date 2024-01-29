# Generated by Django 3.2.9 on 2022-01-20 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("guests", "0001_create_guest_profile"),
        ("charter", "0031_renamed_temp_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="guestdetail",
            name="profile",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="details",
                to="guests.guestprofile",
            ),
        ),
    ]