import pytest

from django.test import Client

from admins.models import AdminProfile
from charter.factories import GuestFactory
from charter.models import GuestDetail
from guests.factories import GuestProfileFactory
from guests.models import GuestProfile
from authentication.models import User
from vessels.factories import VesselFactory


@pytest.fixture()
def admin_user():
    user = User.objects.create(
        email="admin@dwm.com",
        first_name="John",
        last_name="Doe-ADMIN",
        role=User.Roles.ADMIN,
        password="admin123123",
    )
    AdminProfile.objects.create(
        user=user,
        phone_number="+111111111",
        role=AdminProfile.Roles.CAPTAIN,
    )
    VesselFactory(admin=user.admin_profile)
    return user


@pytest.fixture()
def admin_client(admin_user):
    client = Client()
    client.force_login(user=admin_user)
    return client


@pytest.fixture
def guest_user():
    user = User.objects.create(
        email="guest@dwm.com",
        role=User.Roles.GUEST,
        password="guest123123",
    )
    guest_profile = GuestProfileFactory(user=user)
    GuestFactory(profile=guest_profile)
    return user


@pytest.fixture
def guest_client(guest_user):
    client = Client()
    client.force_login(guest_user)
    return client


@pytest.fixture
def unauthenticated_client():
    return Client()
