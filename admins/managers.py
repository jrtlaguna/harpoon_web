from authentication.managers import UserManager
from authentication.models import User


class AdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Roles.ADMIN, is_superuser=False)
