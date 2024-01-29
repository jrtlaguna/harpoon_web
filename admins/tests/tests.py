import pytest

from admins.models import AdminProfile, AdminNotification
from admins.services import (
    create_admin_account,
    get_or_create_incomplete_notification,
    get_or_create_guest_completed_notification,
    update_admin_settings,
)
from authentication.models import User
from charter.factories import CharterFactory


@pytest.mark.django_db
def test_can_create_new_admin_accounts():
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "jdoe@example.com",
        "role": AdminProfile.Roles.CAPTAIN,
        "phone_number": "+123456789",
        "password": "p@ssword!",
    }

    admin = create_admin_account(**data)

    assert admin.first_name == data["first_name"]
    assert admin.last_name == data["last_name"]
    assert admin.email == data["email"]

    # An AdminProfile instance will be created as well.
    assert admin.admin_profile.role == data["role"]
    assert admin.admin_profile.phone_number == data["phone_number"]


@pytest.mark.django_db
def test_can_update_a_users_settings():
    admin = User.objects.create(
        email="test@example.com",
        first_name="John",
        last_name="Doe",
    )
    AdminProfile.objects.create(
        user=admin,
        phone_number="+123456789",
        role=AdminProfile.Roles.CAPTAIN,
        receive_email_notifications=True,
    )

    updated_data = {
        "email": "updated@example.com",
        "first_name": "Adam",
        "last_name": "Smith",
        "phone_number": "+987654321",
        "role": AdminProfile.Roles.PURSER,
        "receive_email_notifications": False,
    }

    update_admin_settings(
        admin=admin,
        **updated_data,
    )

    admin.refresh_from_db()
    admin.admin_profile.refresh_from_db()

    assert updated_data["email"] == admin.email
    assert updated_data["first_name"] == admin.first_name
    assert updated_data["last_name"] == admin.last_name
    assert updated_data["phone_number"] == admin.admin_profile.phone_number

    assert updated_data["role"] == admin.admin_profile.role
    assert (
        updated_data["receive_email_notifications"]
        == admin.admin_profile.receive_email_notifications
    )


@pytest.mark.django_db
def test_get_or_create_incomplete_notification():

    charter = CharterFactory()
    data = {
        "charter": charter,
        "notification_type": AdminNotification.NotificationTypes._1_WEEK_NOTICE,
    }
    notification, created = get_or_create_incomplete_notification(**data)

    assert created
    assert notification.charter == data["charter"]
    assert notification.admin == data["charter"].vessel.admin
    assert notification.notification_type == data["notification_type"]


@pytest.mark.django_db
def test_get_or_create_complete_notification():

    charter = CharterFactory()
    notification, created = get_or_create_guest_completed_notification(charter=charter)

    assert created
    assert notification.charter == charter
    assert notification.admin == charter.vessel.admin
    assert (
        notification.notification_type
        == AdminNotification.NotificationTypes.COMPLETED_PREFERENCE
    )
    assert notification.guest_list is None
