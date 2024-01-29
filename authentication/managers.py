from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(
            email, password, **extra_fields, is_superuser=False, is_staff=False
        )

    def create_superuser(self, email, password, **extra_fields):
        User = get_user_model()
        return self._create_user(
            email,
            password,
            **extra_fields,
            role=User.Roles.ADMIN,
            is_superuser=True,
            is_staff=True
        )
