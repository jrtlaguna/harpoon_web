# Generated by Django 3.2.9 on 2021-12-01 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("charter", "0004_alter_vessel_related_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="FoodPreferences",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("general_cuisine", models.CharField(max_length=255)),
                ("general_cuisine_notes", models.TextField()),
                ("fish_and_shellfish", models.CharField(max_length=255)),
                ("meat", models.CharField(max_length=255)),
                ("meat_notes", models.TextField()),
                ("bread", models.CharField(max_length=255)),
                ("bread_notes", models.TextField()),
                ("salad", models.CharField(max_length=255)),
                ("soup", models.CharField(max_length=255)),
                ("cheese", models.CharField(max_length=255)),
                ("dessert", models.CharField(max_length=255)),
                (
                    "guest",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="food_preferences",
                        to="charter.guest",
                    ),
                ),
            ],
        ),
    ]
