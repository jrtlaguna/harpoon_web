# Generated by Django 3.2.9 on 2022-02-03 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("charter", "0033_charter_currency"),
    ]

    operations = [
        migrations.AlterField(
            model_name="guestdetail",
            name="allergies",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="guestdetail",
            name="medical_issues",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="guestdetail",
            name="medications",
            field=models.TextField(blank=True, null=True),
        ),
    ]