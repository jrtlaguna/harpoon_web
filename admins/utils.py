import ast
import datetime
from typing import List, Tuple
from xmlrpc.client import Boolean

from django.db.models import Q, QuerySet
from django.utils import timezone

from admins.models import AdminNotification, AdminProfile
from admins.services import (
    get_or_create_guest_completed_notification,
    get_or_create_incomplete_notification,
)
from charter.helpers import send_email_template
from charter.models import Charter, GuestDetail

ONE_WEEK_AGO: datetime.datetime = timezone.now() + datetime.timedelta(days=7)
TWO_WEEKS_AGO: datetime.datetime = timezone.now() + datetime.timedelta(days=14)
THREE_WEEKS_AGO: datetime.datetime = timezone.now() + datetime.timedelta(days=21)


def get_two_week_notice(admin: AdminProfile):
    notification_type = AdminNotification.NotificationTypes._2_WEEK_NOTICE
    charters: QuerySet(Charter) = Charter.objects.filter(
        Q(vessel__admin=admin),
        Q(embark_date__lte=TWO_WEEKS_AGO),
        ~Q(notifications__notification_type=notification_type),
    )
    charter_notification_to_generate: List(Charter) = [
        charter for charter in charters if charter.incomplete_unregistered_guests
    ]
    generate_incomplete_notification(
        charters=charter_notification_to_generate,
        notification_type=notification_type,
    )


def get_one_week_notice(admin: AdminProfile):
    notification_type = AdminNotification.NotificationTypes._1_WEEK_NOTICE
    charters: QuerySet(Charter) = Charter.objects.filter(
        Q(vessel__admin=admin),
        Q(embark_date__lte=ONE_WEEK_AGO),
        ~Q(notifications__notification_type=notification_type),
    )
    charter_notification_to_generate: List[Charter] = [
        charter for charter in charters if charter.incomplete_unregistered_guests
    ]
    generate_incomplete_notification(
        charter_notification_to_generate, notification_type=notification_type
    )


def generate_incomplete_notification(
    charters: List[Charter],
    notification_type: AdminNotification.NotificationTypes,
) -> None:
    for charter in charters:
        notification: AdminNotification
        created: bool
        notification, created = get_or_create_incomplete_notification(
            notification_type=notification_type,
            admin=charter.vessel.admin,
            charter=charter,
        )
        if not created:
            notification.guest_list = charter.incomplete_unregistered_guests
            notification.save(update_fields=["guest_list"])


def generate_guest_completed_preference(guest: GuestDetail) -> None:
    today = timezone.now()
    charters: QuerySet(Charter) = guest.charters.filter(disembark_date__gte=today)
    if charters:
        generate_completed_notification(
            charters=charters,
            notification_type=AdminNotification.NotificationTypes.COMPLETED_PREFERENCE,
            guest=guest,
        )


def generate_completed_notification(
    charters: QuerySet(Charter),
    guest: GuestDetail,
) -> None:
    for charter in charters:
        notification: AdminNotification
        created: bool

        notification, created = get_or_create_guest_completed_notification(
            charter=charter,
        )
        if not created:
            if not notification.guest_list:
                notification.guest_list = str([guest.notification_name])
            else:
                try:
                    guest_list = ast.literal_eval(notification.guest_list)
                    guest_list.append(guest.notification_name)
                    notification.guest_list = str(guest_list)
                except Exception as e:
                    print(e)
        else:
            notification.guest_list = str([guest.notification_name])
        notification.save(update_fields=["guest_list"])


def get_admin_notifications(
    admin,
) -> Tuple[QuerySet[AdminNotification], Boolean]:
    notifications = admin.notifications.filter(
        updated_at__lte=THREE_WEEKS_AGO
    ).order_by("-updated_at")

    return notifications[:10], notifications.filter(seen=False).exists()


def guest_send_one_week_notice(charter):
    recipients = list(charter.guests.values_list("email", flat=True))
    subject = f"Pack your bags for {charter.vessel}!"
    data = {"charter": charter}
    send_email_template(
        recipients=recipients,
        template="charter/email/one_week_notice.html",
        data=data,
        subject=subject,
    )


def guest_send_post_trip_notice(charter):
    recipients = list(
        charter.guests.filter(profile__isnull=True).values_list("email", flat=True)
    )
    subject = f"We hope you enjoyed your trip aboard {charter.vessel}!"
    data = {"charter": charter}
    if recipients:
        send_email_template(
            recipients=recipients,
            template="charter/email/post_trip_notice.html",
            data=data,
            subject=subject,
        )
