# Generated by Django 3.2.9 on 2021-12-21 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("charter", "0012_charter_is_complete"),
    ]

    operations = [
        migrations.AlterField(
            model_name="charter",
            name="disembark_location",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="charter",
            name="embark_location",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]