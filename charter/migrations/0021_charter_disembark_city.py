# Generated by Django 3.2.9 on 2022-01-13 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("charter", "0020_alter_dietservicessizespreferences_shirt_size"),
    ]

    operations = [
        migrations.AddField(
            model_name="charter",
            name="disembark_city",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]