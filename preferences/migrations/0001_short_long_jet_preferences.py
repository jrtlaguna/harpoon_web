# Generated by Django 3.2.9 on 2022-07-08 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("charter", "0039_short_long_jet_preferences"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShortJetPreferenceSheet",
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
                    "dietary_restrictions",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("VEGAN", "Vegan"),
                            ("PALEO", "Paleo"),
                            ("VEGETARIAN", "Vegetarian"),
                            ("PESCETARIAN", "Pescetarian"),
                            ("GLUTEN_FREE", "Gluten Free"),
                            ("NONE", "None"),
                            ("OTHER", "Other"),
                        ],
                        max_length=50,
                        null=True,
                        verbose_name="Dietary Restrications",
                    ),
                ),
                (
                    "dietary_restrictions_notes",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "dietary_restrictions_other_notes",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "breakfast",
                    models.CharField(
                        blank=True, max_length=250, null=True, verbose_name="Breakfast"
                    ),
                ),
                (
                    "breakfast_notes",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Breakfast Notes",
                    ),
                ),
                (
                    "lunch",
                    models.CharField(
                        blank=True, max_length=250, null=True, verbose_name="Lunch"
                    ),
                ),
                (
                    "lunch_notes",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Lunch Notes",
                    ),
                ),
                (
                    "dinner",
                    models.CharField(
                        blank=True, max_length=250, null=True, verbose_name="Dinner"
                    ),
                ),
                (
                    "dinner_notes",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Dinner Notes",
                    ),
                ),
                (
                    "guest",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="short_jet_preference",
                        to="charter.guestdetail",
                        verbose_name="Guest",
                    ),
                ),
            ],
            options={
                "verbose_name": "Short Jet Preference Sheet",
                "verbose_name_plural": "Short Jet Preference Sheets",
            },
        ),
        migrations.CreateModel(
            name="LongJetPreferenceSheet",
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
                    "dietary_restrictions",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("VEGAN", "Vegan"),
                            ("PALEO", "Paleo"),
                            ("VEGETARIAN", "Vegetarian"),
                            ("PESCETARIAN", "Pescetarian"),
                            ("GLUTEN_FREE", "Gluten Free"),
                            ("NONE", "None"),
                            ("OTHER", "Other"),
                        ],
                        max_length=50,
                        null=True,
                        verbose_name="Dietary Restrications",
                    ),
                ),
                (
                    "dietary_restrictions_notes",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "dietary_restrictions_other_notes",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "breakfast",
                    models.CharField(
                        blank=True, max_length=250, null=True, verbose_name="Breakfast"
                    ),
                ),
                (
                    "breakfast_notes",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Breakfast Notes",
                    ),
                ),
                (
                    "lunch",
                    models.CharField(
                        blank=True, max_length=250, null=True, verbose_name="Lunch"
                    ),
                ),
                (
                    "lunch_notes",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Lunch Notes",
                    ),
                ),
                (
                    "dinner",
                    models.CharField(
                        blank=True, max_length=250, null=True, verbose_name="Dinner"
                    ),
                ),
                (
                    "dinner_notes",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Dinner Notes",
                    ),
                ),
                (
                    "fresh_snacks",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Fresh Snacks",
                    ),
                ),
                (
                    "fresh_snacks_notes",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Fresh Snacks Notes",
                    ),
                ),
                (
                    "pantry_snacks",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Pantry Snacks",
                    ),
                ),
                (
                    "pantry_snacks_notes",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="Pantry Snacks Notes",
                    ),
                ),
                (
                    "guest",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="long_jet_preference",
                        to="charter.guestdetail",
                        verbose_name="Guest",
                    ),
                ),
            ],
            options={
                "verbose_name": "Long Jet Preference Sheet",
                "verbose_name_plural": "Long Jet Preference Sheets",
            },
        ),
    ]
