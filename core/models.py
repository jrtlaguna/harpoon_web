from django.apps import apps
from django.db import models
from django.db.models.base import ModelBase


class Document(models.Model):
    class ModelChoices(models.TextChoices):
        GUEST_DETAIL = ("GUEST_DETAIL", "Guest Detail")
        VESSEL = ("VESSEL", "Vessel")

    document = models.FileField(verbose_name="Document")
    model = models.CharField(
        verbose_name="Model",
        choices=ModelChoices.choices,
        max_length=256,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )
    model_id = models.IntegerField(verbose_name="Model Id")
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
    )
    uploaded_by = models.ForeignKey(
        "authentication.User",
        verbose_name="Uploaded By",
        related_name="documents",
        on_delete=models.CASCADE,
    )

    def get_model(self, model: str) -> ModelBase:

        if model == self.ModelChoices.GUEST_DETAIL:
            return apps.get_model("charter", "GuestDetail")
        elif model == self.ModelChoices.VESSEL:
            return apps.get_model("vessels", "Vessel")
        else:
            raise ValueError("Invalid model value.")

    def __str__(self):
        return f"{self.model} - {self.uploaded_by} - {self.document.name}"

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
