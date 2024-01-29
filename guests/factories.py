import factory

from admins.factories import UserFactory
from guests.models import GuestProfile


class GuestProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    phone_number = "+111111111"

    class Meta:
        model = GuestProfile
