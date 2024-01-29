from datetime import datetime, timedelta

from django.db.models import QuerySet
from django.utils import timezone

from admins.models import AdminProfile
from admins.utils import (
    generate_guest_completed_preference,
    get_one_week_notice,
    get_two_week_notice,
    guest_send_one_week_notice,
)
from charter.models import Charter, GuestDetail
from config.celery import app


@app.task(serializer="json")
def generate_one_week_notice() -> None:
    admins: QuerySet(AdminProfile) = AdminProfile.objects.all()
    for admin in admins:
        get_one_week_notice(admin)


@app.task(serializer="json")
def generate_two_week_notice() -> None:
    admins: QuerySet(AdminProfile) = AdminProfile.objects.all()
    for admin in admins:
        get_two_week_notice(admin)


@app.task(serializer="json")
def has_completed_preferences(guest_id: int) -> None:
    try:
        guest: GuestDetail = GuestDetail.objects.get(id=guest_id)
        if not guest.is_incomplete:
            generate_guest_completed_preference(guest)

    except GuestDetail.DoesNotExist as err:
        print(err)


@app.task(serializer="json")
def email_one_week_notice() -> None:

    ONE_WEEK_FROM_TODAY = (timezone.now() + timedelta(days=7)).date()
    try:
        charters: QuerySet(Charter) = Charter.objects.filter(
            embark_date=ONE_WEEK_FROM_TODAY
        )
        for charter in charters:
            guest_send_one_week_notice(charter)
    except Exception as err:
        print(err)


@app.task(serializer="json")
def email_post_trip_notice() -> None:

    TWO_DAYS_AFTER = (timezone.now() + timedelta(days=2)).date()
    try:
        charters: QuerySet(Charter) = Charter.objects.filter(
            disembark_date=TWO_DAYS_AFTER
        )
        for charter in charters:
            guest_send_one_week_notice(charter)
    except Exception as err:
        print(err)
