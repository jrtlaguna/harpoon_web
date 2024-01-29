import factory

from admins.factories import AdminProfileFactory
from vessels.models import Vessel


class VesselFactory(factory.django.DjangoModelFactory):
    name = "Odessa"
    charter_type = Vessel.CharterType.MOTOR_YACHT
    imo_number = "23123"
    admin = factory.SubFactory(AdminProfileFactory)

    class Meta:
        model = Vessel
