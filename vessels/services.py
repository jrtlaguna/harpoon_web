from admins.models import AdminProfile
from vessels.models import Vessel


def create_vessel(
    *,
    name: str,
    charter_type: Vessel.CharterType,
    imo_number: str,
    admin: AdminProfile,
) -> Vessel:
    """
    Creates an Vessel given the details provided.
    """
    vessel = Vessel.objects.create(
        name=name,
        charter_type=charter_type,
        imo_number=imo_number,
        admin=admin,
    )

    return vessel


def update_vessel(
    *,
    vessel: Vessel,
    name: str,
    charter_type: str,
    imo_number: str,
) -> Vessel:
    """
    Updates the Vessel instance based on the details provided.
    """
    vessel.name = name
    vessel.charter_type = charter_type
    vessel.imo_number = imo_number
    vessel.save()
    return vessel
