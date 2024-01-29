from datetime import datetime, timedelta
from typing import Any, Sequence

from django.contrib.auth import get_user_model
import factory
from factory import post_generation

from vessels.factories import VesselFactory
from charter.models import Charter, GuestDetail


class UserFactory(factory.django.DjangoModelFactory):
    email = "admin@mail.com"

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = "password"
        self.set_password(password)

    class Meta:
        model = get_user_model()


class CharterFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    vessel = factory.SubFactory(VesselFactory)
    apa_budget = 10000
    embark_date = datetime.now().date()
    embark_time = "08:00 am"
    embark_name_of_dock = "Tortolla Yacht Club"
    embark_city = "Rio"
    embark_country = "Brazil"
    disembark_date = (datetime.now() + timedelta(days=10)).date()
    disembark_time = "11:00 pm"
    disembark_name_of_dock = "Tortolla Yacht Club"
    disembark_country = "Brazil"
    booking_id = "1XYZ001"
    is_complete = True

    class Meta:
        model = Charter


class GuestFactory(factory.django.DjangoModelFactory):
    charter = factory.RelatedFactoryList(CharterFactory, size=1)
    first_name = "John"
    last_name = "Doe"
    email = "john.doe@email.com"

    class Meta:
        model = GuestDetail
