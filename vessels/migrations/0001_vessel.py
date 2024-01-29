# Generated by Django 3.2.9 on 2021-11-24 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("admins", "0002_add_receive_email_notifications"),
    ]

    operations = [
        migrations.CreateModel(
            name="Vessel",
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
                    "name",
                    models.CharField(max_length=250, verbose_name="Name of Vessel"),
                ),
                (
                    "charter_type",
                    models.CharField(
                        choices=[
                            ("MOTOR YACHT", "Motor Yacht"),
                            ("CATARMAN", "Catarman"),
                            ("SAIL YACHT", "Sail Yacht"),
                            ("FISHING", "Fishing"),
                            ("RIB", "Rib"),
                        ],
                        max_length=50,
                        verbose_name="Charter Type",
                    ),
                ),
                ("crew_size", models.PositiveIntegerField(verbose_name="Crew Size")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "admin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vessels",
                        to="admins.adminprofile",
                        verbose_name="Admin",
                    ),
                ),
            ],
            options={
                "verbose_name": "Vessel",
                "verbose_name_plural": "Vessels",
            },
        ),
    ]