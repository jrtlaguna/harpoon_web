import datetime

from django.db import models, transaction
from django.utils import timezone

from core.models import Document


class Vessel(models.Model):
    """
    Contains the information for a Vessel.
    """

    class CharterType(models.TextChoices):
        MOTOR_YACHT = ("M/Y", "Motor Yacht")
        CATARMAN = ("C", "Catamaran")
        SAIL_YACHT = ("S/Y", "Sail Yacht")
        FISHING = ("F", "Fishing")
        TINDER = ("T", "Tinder")

    name = models.CharField(
        "Name of Vessel",
        max_length=250,
    )
    charter_type = models.CharField(
        "Charter Type",
        max_length=50,
        choices=CharterType.choices,
    )
    admin = models.ForeignKey(
        "admins.AdminProfile",
        related_name="vessels",
        verbose_name="Admin",
        on_delete=models.CASCADE,
    )
    crew_members = models.ManyToManyField(
        "admins.AdminProfile",
        verbose_name="Crew Members",
    )
    imo_number = models.CharField(
        verbose_name="International Maritime Organization #",
        max_length=50,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(verbose_name="Active", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vessel"
        verbose_name_plural = "Vessels"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.is_active:
            if not self.admin.vessels.exists():
                self.is_active = True
            return super(Vessel, self).save(*args, **kwargs)
        with transaction.atomic():
            Vessel.objects.filter(is_active=True, admin=self.admin).update(
                is_active=False
            )
            if self.admin not in self.crew_members.all():
                self.crew_members.add(self.admin)
            return super(Vessel, self).save(*args, **kwargs)

    @property
    def proper_name(self):
        if self.charter_type == "C":
            proper_name = f"{self.get_charter_type_display()} {self.name}"
        else:
            proper_name = f"{self.charter_type} {self.name}"
        return proper_name

    @property
    def has_upcoming_trips(self):
        one_week_from_now = timezone.now() + datetime.timedelta(days=7)
        return self.charters.filter(embark_date__lte=one_week_from_now).exists()

    @property
    def documents(self):
        return Document.objects.filter(
            model_id=self.id, model=Document.ModelChoices.VESSEL
        )


# class CrewMembership(models.Model):
#     class Meta:
#         verbose_name = "Crew Membership"
#         verbose_name_plural = "Crew Memberships"

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
