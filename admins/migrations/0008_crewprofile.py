# Generated by Django 3.2.9 on 2023-02-22 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("admins", "0007_alter_adminprofile_role"),
    ]

    operations = [
        migrations.CreateModel(
            name="CrewProfile",
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
                    "crew_type",
                    models.CharField(
                        choices=[
                            ("DECKHAND", "Deckhand/Second Engineer"),
                            ("CAPTAIN", "Captain"),
                            ("FIRST_OFFICER", "First Officer"),
                            ("CHIEF_STEWARD", "Chief Steward/ess"),
                            ("PURSER", "Purser"),
                            ("ENGINEER", "Engineer"),
                        ],
                        max_length=40,
                        verbose_name="Crew Type",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=256, verbose_name="First Name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=256, verbose_name="Last Name"),
                ),
                (
                    "previous_yacht",
                    models.CharField(max_length=400, verbose_name="Previous Yacht"),
                ),
                ("interest", models.CharField(max_length=256, verbose_name="Interest")),
                ("about", models.CharField(max_length=256, verbose_name="About")),
                (
                    "admin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="crew_members",
                        to="admins.adminprofile",
                        verbose_name="Admin",
                    ),
                ),
            ],
            options={
                "verbose_name": "Crew Profile",
                "verbose_name_plural": "Crew Profiles",
            },
        ),
    ]