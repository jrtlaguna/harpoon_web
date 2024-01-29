import pytest

from admins.models import AdminProfile
from admins.factories import AdminProfileFactory
from vessels.models import Vessel
from vessels.services import create_vessel, update_vessel
from vessels.factories import VesselFactory


@pytest.mark.django_db
def test_can_create_new_vessel(admin_user):
    admin_profile: AdminProfile = admin_user.admin_profile
    data = {
        "name": "Odessa",
        "charter_type": Vessel.CharterType.MOTOR_YACHT,
        "imo_number": "123456",
        "admin": admin_profile,
    }

    vessel: Vessel = create_vessel(**data)

    assert vessel.admin == data["admin"]
    assert vessel.name == data["name"]
    assert vessel.charter_type == data["charter_type"]
    assert vessel.imo_number == data["imo_number"]


@pytest.mark.django_db
def test_can_update_existing_vessel():
    vessel: Vessel = VesselFactory()
    data = {
        "name": "Black Pearl",
        "charter_type": Vessel.CharterType.SAIL_YACHT,
        "imo_number": "123456",
    }

    vessel: Vessel = update_vessel(vessel=vessel, **data)
    vessel.refresh_from_db()

    assert vessel.name == data["name"]
