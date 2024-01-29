from annoying.functions import get_object_or_None

from charter.models import Charter, GuestDetail
from vessels.models import Vessel
from authentication.models import User


def create_charter_details(
    *,
    created_by: User,
    vessel: Vessel,
    first_name: str,
    last_name: str,
    email: str,
    apa_budget: float,
    currency: str,
    embark_city: str,
    embark_country: str,
    embark_date: str,
    disembark_date: str,
    booking_id: str,
) -> Charter:
    """
    Creates charter with charter details as initial data and creates principal guest
    """
    if not (principal_guest := get_object_or_None(GuestDetail, email=email)):
        principal_guest = GuestDetail.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
    charter = Charter.objects.create(
        principal_guest=principal_guest,
        apa_budget=apa_budget,
        currency=currency,
        embark_city=embark_city,
        embark_country=embark_country,
        embark_date=embark_date,
        disembark_date=disembark_date,
        booking_id=booking_id,
        created_by=created_by,
        vessel=vessel,
    )

    return charter


def update_charter_details(
    *,
    charter: Charter,
    first_name: str,
    last_name: str,
    email: str,
    apa_budget: float,
    currency: str,
    embark_city: str,
    embark_country: str,
    embark_date: str,
    disembark_date: str,
):
    """
    Updates the charter and principal guest with the given details.
    """
    if charter.principal_guest.email != email:
        if not (principal_guest := get_object_or_None(GuestDetail, email=email)):
            principal_guest = GuestDetail.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            charter.principal_guest = principal_guest
        else:
            charter.principal_guest.first_name = first_name
            charter.principal_guest.last_name = last_name
            charter.principal_guest = principal_guest
            charter.principal_guest.save()
            if principal_guest in charter.guests.all():
                charter.guests.remove(principal_guest)
    charter.apa_budget = apa_budget
    charter.currency = currency
    charter.embark_city = embark_city
    charter.embark_country = embark_country
    charter.embark_date = embark_date
    charter.disembark_date = disembark_date

    charter.save()

    return charter


def update_charter_locations(
    *,
    charter: Charter,
    embark_name_of_dock: str,
    embark_city: str,
    embark_country: str,
    embark_additional_info: str,
    embark_date: str,
    embark_time: str,
    disembark_name_of_dock: str,
    disembark_city: str,
    disembark_country: str,
    disembark_additional_info: str,
    disembark_date: str,
    disembark_time: str,
):
    """
    Updates the charter with the given charter locations.
    """
    charter.embark_name_of_dock = embark_name_of_dock
    charter.embark_city = embark_city
    charter.embark_country = embark_country
    charter.embark_additional_info = embark_additional_info
    charter.embark_date = embark_date
    charter.embark_time = embark_time
    charter.disembark_name_of_dock = disembark_name_of_dock
    charter.disembark_city = disembark_city
    charter.disembark_country = disembark_country
    charter.disembark_additional_info = disembark_additional_info
    charter.disembark_date = disembark_date
    charter.disembark_time = disembark_time
    charter.save()

    return charter


def update_trip_details(
    *,
    charter: Charter,
    first_name: str,
    last_name: str,
    email: str,
    apa_budget: float,
    currency: str,
    embark_name_of_dock: str,
    embark_city: str,
    embark_country: str,
    embark_additional_info: str,
    embark_date: str,
    embark_time: str,
    disembark_name_of_dock: str,
    disembark_city: str,
    disembark_country: str,
    disembark_additional_info: str,
    disembark_date: str,
    disembark_time: str,
):
    """
    Updates the trip details with the given details.
    """
    if charter.principal_guest.email != email:
        if not (principal_guest := get_object_or_None(GuestDetail, email=email)):
            principal_guest = GuestDetail.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            charter.principal_guest = principal_guest
    else:
        charter.principal_guest.first_name = first_name
        charter.principal_guest.last_name = last_name
        charter.principal_guest.save()

    charter.apa_budget = apa_budget
    charter.currency = currency
    charter.embark_name_of_dock = embark_name_of_dock
    charter.embark_city = embark_city
    charter.embark_country = embark_country
    charter.embark_additional_info = embark_additional_info
    charter.embark_date = embark_date
    charter.embark_time = embark_time
    charter.disembark_name_of_dock = disembark_name_of_dock
    charter.disembark_city = disembark_city
    charter.disembark_country = disembark_country
    charter.disembark_additional_info = disembark_additional_info
    charter.disembark_date = disembark_date
    charter.disembark_time = disembark_time
    charter.save()

    return charter


def add_guests_email(
    *,
    charter: Charter,
    email: str,
) -> GuestDetail:
    """
    Creates additional guest for the given charter
    """
    guest, created = GuestDetail.objects.get_or_create(email=email)
    charter.guests.add(guest)
    return guest


def complete_charter_setup(
    *,
    charter: Charter,
    is_complete: bool,
):
    charter.is_complete = is_complete
    charter.save()

    return charter
