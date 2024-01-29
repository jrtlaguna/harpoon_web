# Generated by Django 3.2.9 on 2021-12-01 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("charter", "0005_foodpreferences"),
    ]

    operations = [
        migrations.CreateModel(
            name="MealAndRoomPreferences",
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
                (
                    "breakfast_time",
                    models.CharField(
                        choices=[
                            ("_0700AM", "07:00 AM"),
                            ("_0730AM", "07:30 AM"),
                            ("_0800AM", "08:00 AM"),
                            ("_0830AM", "08:30 AM"),
                        ],
                        max_length=255,
                    ),
                ),
                ("breakfast_note", models.TextField()),
                (
                    "lunch_time",
                    models.CharField(
                        choices=[
                            ("_1100AM", "11:00 AM"),
                            ("_1130AM", "11:30 AM"),
                            ("_1200PM", "12:00 PM"),
                            ("_1230PM", "12:30 PM"),
                        ],
                        max_length=255,
                    ),
                ),
                ("lunch_note", models.TextField()),
                (
                    "dinner_time",
                    models.CharField(
                        choices=[
                            ("_0600PM", "06:00 PM"),
                            ("_0630PM", "06:30 PM"),
                            ("_0700PM", "07:00 PM"),
                            ("_0730PM", "07:30 PM"),
                        ],
                        max_length=255,
                    ),
                ),
                ("dinner_note", models.TextField()),
                (
                    "canapes_time",
                    models.CharField(
                        choices=[
                            ("BEFORE_LUNCH", "Before Lunch"),
                            ("BEFORE_DINNER", "Before Dinner"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "canapes_selection",
                    models.CharField(
                        choices=[
                            ("LIGHT", "Light"),
                            ("FULL_SELECTION", "Full Selection"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "midmorning_snacks",
                    models.CharField(
                        choices=[("SWEET", "Sweet"), ("SAVORY", "Savory")],
                        max_length=255,
                    ),
                ),
                (
                    "midafternoon_snacks",
                    models.CharField(
                        choices=[("SWEET", "Sweet"), ("SAVORY", "Savory")],
                        max_length=255,
                    ),
                ),
                ("favorite_flowers", models.CharField(max_length=255)),
                (
                    "guest",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="meal_and_room_preferences",
                        to="charter.guest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LunchSelection",
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
                ("name", models.CharField(max_length=255)),
                (
                    "meal_and_room_preferences",
                    models.ManyToManyField(
                        related_name="lunch_selections",
                        to="charter.MealAndRoomPreferences",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DinnerSelection",
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
                ("name", models.CharField(max_length=255)),
                (
                    "meal_and_room_preferences",
                    models.ManyToManyField(
                        related_name="dinner_selections",
                        to="charter.MealAndRoomPreferences",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BreakfastSelection",
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
                ("name", models.CharField(max_length=255)),
                (
                    "meal_and_room_preferences",
                    models.ManyToManyField(
                        related_name="breakfast_selections",
                        to="charter.MealAndRoomPreferences",
                    ),
                ),
            ],
        ),
    ]
