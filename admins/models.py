from django.conf import settings
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from admins.managers import AdminManager
from authentication.models import User
from charter.models import Charter


class Admin(User):
    """
    Proxy model for administrators.
    """

    class Meta:
        proxy = True

    objects = AdminManager()


class AdminProfile(models.Model):
    """
    Contains the information for an admin account.
    """

    class Roles(models.TextChoices):
        CAPTAIN = ("CAPTAIN", "Captain")
        FIRST_OFFICER = ("FIRST_OFFICER", "First Officer")
        CHIEF_STEWARD = ("CHIEF_STEWARD", "Chief Steward/ess")
        PURSER = ("PURSER", "Purser")
        OTHER = ("OTHER", "Other")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="admin_profile"
    )
    phone_number = models.CharField(max_length=25)
    role = models.CharField(max_length=255, choices=Roles.choices)
    receive_email_notifications = models.BooleanField(default=True)

    @property
    def is_admin(self):
        return self.role == self.Roles.CAPTAIN

    @property
    def upcoming_charters(self) -> QuerySet(Charter):
        today = timezone.now()
        return Charter.objects.filter(
            vessel__id__in=self.vessels.values_list("id"), disembark_date__gte=today
        )

    def __str__(self):
        return str(self.user)


class AdminNotification(models.Model):
    class NotificationTypes(models.TextChoices):
        _1_WEEK_NOTICE = ("1_WEEK_NOTICE", "1 Week Notice")
        _2_WEEK_NOTICE = ("2_WEEK_NOTICE", "2 Week Notice")
        COMPLETED_PREFERENCE = ("COMPLETED_PREFERENCE", "Completed Preference")

    notification_type = models.CharField(
        verbose_name="Notification Type",
        max_length=250,
        choices=NotificationTypes.choices,
    )
    admin = models.ForeignKey(
        "admins.AdminProfile",
        related_name="notifications",
        verbose_name="Admin",
        on_delete=models.CASCADE,
    )
    charter = models.ForeignKey(
        "charter.Charter",
        related_name="notifications",
        verbose_name="Charter",
        on_delete=models.CASCADE,
    )
    guest_list = models.CharField(
        verbose_name="Guest List",
        max_length=250,
        blank=True,
        null=True,
    )
    seen = models.BooleanField(verbose_name="Seen", default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f"{self.admin} - {self.charter} - {self.notification_type}"

    class Meta:
        verbose_name = "Admin Notification"
        verbose_name_plural = "Admin Notifications"


class CrewProfile(models.Model):
    class CrewTypes(models.TextChoices):
        DECKHAND = ("DECKHAND", "Deckhand/Second Engineer")
        CAPTAIN = ("CAPTAIN", "Captain")
        FIRST_OFFICER = ("FIRST_OFFICER", "First Officer")
        CHIEF_STEWARD = ("CHIEF_STEWARD", "Chief Steward/ess")
        PURSER = ("PURSER", "Purser")
        ENGINEER = ("ENGINEER", "Engineer")

    crew_type = models.CharField(
        verbose_name="Crew Type",
        max_length=40,
        choices=CrewTypes.choices,
    )
    first_name = models.CharField(verbose_name="First Name", max_length=256)
    last_name = models.CharField(verbose_name="Last Name", max_length=256)
    previous_yacht = models.CharField(
        verbose_name="Previous Yacht",
        max_length=400,
        null=True,
        blank=True,
    )
    interest = models.CharField(
        verbose_name="Interest",
        max_length=256,
        null=True,
        blank=True,
    )
    about = models.TextField(
        verbose_name="About",
        null=True,
        blank=True,
    )
    admin = models.ForeignKey(
        "admins.AdminProfile",
        verbose_name="Admin",
        related_name="crew_members",
        on_delete=models.CASCADE,
    )
    profile_picture = models.ImageField(
        "Profile Picture",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.get_crew_type_display()}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Crew Profile"
        verbose_name_plural = "Crew Profiles"


class GenderChoices(models.TextChoices):
    MALE = ("MALE", "Male")
    FEMALE = ("FEMALE", "Female")
    TRANSGENDER = ("TRANSGENDER", "Female")
    NON_BINARY = ("NON_BINARY", "Non-binary/Non-Conforming")
    NO_RESPONSE = ("NO_RESPONSE", "Prefer not to respond")


class GuestInformation(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=256)
    last_name = models.CharField(verbose_name="Last Name", max_length=256)
    email = models.EmailField(verbose_name="Email", null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        verbose_name="Gender",
        max_length=52,
        choices=GenderChoices.choices,
        null=True,
        blank=True,
    )
    contact_number = models.CharField(max_length=25, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    nationality = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    admin = models.ForeignKey(
        "admins.AdminProfile",
        verbose_name="Admin",
        related_name="admin_guest_information",
        on_delete=models.CASCADE,
    )
    profile_picture = models.ImageField(
        "Profile Picture",
        null=True,
        blank=True,
    )

    def __str__(self):
        name = f"{self.last_name}, {self.first_name}"
        if self.email:
            name = f"{name} / {self.email}"
        return name

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Guest Information"
        verbose_name_plural = "Guest Information"
