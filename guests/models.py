from django.conf import settings
from django.db import models

from authentication.models import User
from guests.managers import GuestManager


class Guest(User):
    """
    Proxy model for guests.
    """

    class Meta:
        proxy = True

    objects = GuestManager()


class GuestProfile(models.Model):
    """
    Contains the information for a guest account.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="guest_profile"
    )
    phone_number = models.CharField(max_length=25)
    receive_email_notifications = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Guest Profile"
        verbose_name_plural = "Guest Profiles"
