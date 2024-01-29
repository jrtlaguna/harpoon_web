from datetime import date
from typing import Optional, Tuple
from xmlrpc.client import boolean

from admins.models import AdminNotification, AdminProfile, CrewProfile, GuestInformation
from authentication.models import User
from charter.models import Charter


def create_admin_account(
    *,
    first_name: str,
    last_name: str,
    email: str,
    role: str,
    phone_number: str,
    password: str,
) -> User:
    """
    Creates an Administrator account given the details provided.
    """
    user = User.objects.create(
        first_name=first_name, last_name=last_name, email=email, role=User.Roles.ADMIN
    )
    user.set_password(password)
    user.save()

    AdminProfile.objects.create(user=user, role=role, phone_number=phone_number)

    return user


def update_admin_settings(
    *,
    admin: User,
    first_name: str,
    last_name: str,
    email: str,
    role: str,
    phone_number: str,
    receive_email_notifications: bool,
):
    """
    Updates the given admin account with the provided details.
    """
    admin.first_name = first_name
    admin.last_name = last_name
    admin.email = email
    admin.admin_profile.role = role
    admin.admin_profile.phone_number = phone_number
    admin.admin_profile.receive_email_notifications = receive_email_notifications

    admin.admin_profile.save()
    admin.save()

    return admin


def get_or_create_incomplete_notification(
    notification_type: AdminNotification.NotificationTypes,
    charter: Charter,
) -> Tuple[AdminNotification, boolean]:
    return AdminNotification.objects.get_or_create(
        notification_type=notification_type,
        admin=charter.vessel.admin,
        charter=charter,
    )


def get_or_create_guest_completed_notification(
    charter: Charter,
) -> Tuple[AdminNotification, boolean]:
    return AdminNotification.objects.get_or_create(
        notification_type=AdminNotification.NotificationTypes.COMPLETED_PREFERENCE,
        charter=charter,
        admin=charter.vessel.admin,
    )


def create_crew_profile(
    admin: AdminProfile,
    first_name: str,
    last_name: str,
    crew_type: str,
    previous_yacht: Optional[str],
    interest: Optional[str],
    about: Optional[str],
):
    return CrewProfile.objects.create(
        admin=admin,
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        crew_type=crew_type,
        previous_yacht=previous_yacht,
        interest=interest,
        about=about,
    )


def edit_crew_profile(
    crew: CrewProfile,
    first_name: str,
    last_name: str,
    crew_type: str,
    previous_yacht: Optional[str],
    interest: Optional[str],
    about: Optional[str],
) -> CrewProfile:
    crew.first_name = first_name.strip()
    crew.last_name = last_name.strip()
    crew.crew_type = crew_type
    crew.previous_yacht = previous_yacht
    crew.interest = interest
    crew.about = about
    crew.save()
    return crew


def create_guest_info(
    admin: AdminProfile,
    first_name: str,
    last_name: str,
    email: str,
    date_of_birth: date,
    gender: str,
    contact_number: str,
    notes: str,
    nationality: str,
):
    return GuestInformation.objects.create(
        admin=admin,
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        email=email,
        date_of_birth=date_of_birth,
        gender=gender,
        contact_number=contact_number,
        notes=notes,
        nationality=nationality,
    )


def edit_guest_info(
    guest_info: GuestInformation,
    first_name: str,
    last_name: str,
    email: str,
    date_of_birth: date,
    gender: str,
    contact_number: str,
    notes: str,
    nationality: str,
) -> GuestInformation:
    guest_info.first_name = first_name.strip()
    guest_info.last_name = last_name.strip()
    guest_info.email = email
    guest_info.date_of_birth = date_of_birth
    guest_info.gender = gender
    guest_info.contact_number = contact_number
    guest_info.notes = notes
    guest_info.nationality = nationality
    guest_info.save()
    return guest_info
