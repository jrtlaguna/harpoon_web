from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from authentication.managers import UserManager


class User(AbstractUser):
    """
    Custom user model.
    """

    class Roles(models.TextChoices):
        ADMIN = ("ADMIN", "ADMIN")
        GUEST = ("GUEST", "GUEST")

    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=255, choices=Roles.choices)
    profile_picture = models.ImageField(
        "Profile Picture",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_guest(self):
        return self.role == self.Roles.GUEST

    @property
    def guest_details(self):
        if self.is_guest:
            return self.guest_profile.details
        return None


def _generate_code():
    return get_random_string(length=4).upper()


def _30_minutes_from_now():
    return timezone.now() + timedelta(minutes=30)


class PasswordResetCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="password_reset_codes",
        on_delete=models.CASCADE,
    )
    code = models.CharField(max_length=4, default=_generate_code)
    expires_at = models.DateTimeField(default=_30_minutes_from_now)

    def __str__(self):
        return self.code

    @property
    def has_expired(self):
        return self.expires_at < timezone.now()
