from typing import Any, Sequence

import factory
from django.contrib.auth import get_user_model
from factory import post_generation

from admins.models import AdminProfile


class UserFactory(factory.django.DjangoModelFactory):
    email = "user@dwm.com"

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = "password"
        self.set_password(password)

    class Meta:
        model = get_user_model()


class AdminProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    role = AdminProfile.Roles.CAPTAIN
    phone_number = "+1xxxxxxxxxxx"

    class Meta:
        model = AdminProfile
