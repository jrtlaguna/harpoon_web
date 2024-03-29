# Generated by Django 3.2.9 on 2022-12-08 02:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
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
                ("document", models.FileField(upload_to="", verbose_name="Document")),
                (
                    "model",
                    models.CharField(
                        choices=[
                            ("GUEST_DETAIL", "Guest Detail"),
                            ("VESSEL", "Vessel"),
                        ],
                        max_length=256,
                        verbose_name="Model",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                ("model_id", models.IntegerField(verbose_name="Model Id")),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "uploaded_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Uploaded By",
                    ),
                ),
            ],
        ),
    ]
