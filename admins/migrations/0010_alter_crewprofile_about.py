# Generated by Django 3.2.9 on 2023-03-03 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admins", "0009_auto_20230222_1123"),
    ]

    operations = [
        migrations.AlterField(
            model_name="crewprofile",
            name="about",
            field=models.TextField(blank=True, null=True, verbose_name="About"),
        ),
    ]
