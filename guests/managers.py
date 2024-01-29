from authentication.managers import UserManager
from authentication.models import User


class GuestManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Roles.GUEST, is_superuser=False)
