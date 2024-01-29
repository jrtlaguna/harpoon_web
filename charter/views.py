from datetime import date, datetime

from annoying.functions import get_object_or_None
from dateutil import parser as ps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from admins.utils import get_admin_notifications
from authentication.decorators import admin_required, guest_required
from authentication.models import User
from authentication.utils import check_emails
from charter.forms import (
    AddGuestForm,
    AddGuestsForm,
    CharterDetailsForm,
    CharterLocationsForm,
    EditTripDetailsForm,
    PreferencesShoppingListForm,
)
from charter.helpers import (
    auto_increment_booking_id,
    extract_meal_times_and_types,
    extract_preferences,
    generate_guest_details_pdf,
    generate_meal_times_and_types_pdf,
    generate_trip_details_pdf,
    get_shopping_list_response,
    send_email_template,
)
from charter.models import Charter, GuestDetail
from charter.services import (
    add_guests_email,
    complete_charter_setup,
    create_charter_details,
    update_charter_details,
    update_charter_locations,
    update_trip_details,
)
from vessels.models import Vessel


@login_required
@admin_required
def charter_details(request: HttpRequest, charter_id: int = None) -> HttpResponse:
    """
    Update a trip
    """
    show_modal = True
    if "admin/dashboard" in request.headers.get("Referer", ""):
        show_modal = False

    breadcrumbs = "Trip Details > Principal Info"

    try:
        charter = Charter.objects.get(id=charter_id)
    except Charter.DoesNotExist:
        messages.error("Charter does not exist.", fail_silently=True)
        return redirect(reverse("admins:dashboard"))

    vessel = charter.vessel

    user: User = request.user
    notifications, new_notifications = get_admin_notifications(
        user.admin_profile,
    )
    ctx = {
        "active": "trips",
        "breadcrumbs": breadcrumbs,
        "notifications": notifications,
        "new_notifications": new_notifications,
        "user": user,
        "show_modal": show_modal,
    }

    if charter_id:
        charter: Charter = get_object_or_404(Charter, id=charter_id)
        ctx["vessel"] = charter.vessel

    if request.method == "POST":
        embark_date = request.POST.get("embark_date")
        disembark_date = request.POST.get("disembark_date")
        if not (disembark_date and embark_date):
            messages.error(request, "Embark/Disembark Date should not be empty.")
            return redirect(reverse("charter:charter_details", args=[charter.id]))
        form = CharterDetailsForm(data=request.POST)
        if form.is_valid():
            if not charter:
                suffix_number = auto_increment_booking_id()
                charter = create_charter_details(
                    first_name=form.cleaned_data["first_name"].capitalize(),
                    last_name=form.cleaned_data["last_name"].capitalize(),
                    email=form.cleaned_data["email"],
                    apa_budget=float(request.POST["apa_budget"].replace(",", "")),
                    currency=request.POST["currency"],
                    embark_city=form.cleaned_data["embark_city"].capitalize(),
                    embark_country=form.cleaned_data["embark_country"].capitalize(),
                    embark_date=datetime.strptime(embark_date, "%d %B %Y"),
                    disembark_date=datetime.strptime(disembark_date, "%d %B %Y"),
                    booking_id=f"{vessel.id}{vessel.name[:3].upper()}{suffix_number}",
                    created_by=user,
                    vessel=vessel,
                )
            else:
                update_charter_details(
                    charter=charter,
                    **form.cleaned_data,
                    apa_budget=float(request.POST["apa_budget"].replace(",", "")),
                    currency=request.POST["currency"],
                    embark_date=datetime.strptime(embark_date, "%d %B %Y"),
                    disembark_date=datetime.strptime(disembark_date, "%d %B %Y"),
                )

            return redirect(reverse("charter:charter_locations", args=[charter.id]))
    else:
        form = CharterDetailsForm()
        if charter:
            form = CharterDetailsForm(
                initial={
                    "first_name": charter.principal_guest.first_name,
                    "last_name": charter.principal_guest.last_name,
                    "email": charter.principal_guest.email,
                    "embark_city": charter.embark_city,
                    "embark_country": charter.embark_country,
                    "embark_date": charter.embark_date,
                    "disembark_date": charter.disembark_date,
                }
            )
            ctx["apa_budget"] = "{:,.2f}".format(charter.apa_budget)
            ctx["currency"] = charter.currency
            ctx["booking_id"] = charter.booking_id
            ctx["charter"] = charter
            ctx["embark_date"] = charter.embark_date.strftime("%d %B %Y")
            ctx["disembark_date"] = charter.disembark_date.strftime("%d %B %Y")
    ctx["form"] = form

    return render(request, "charter/charter_details.html", ctx)


@login_required
@admin_required
def new_trip(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    if not (
        vessel := Vessel.objects.filter(
            admin=user.admin_profile,
            is_active=True,
        )
        .order_by("created_at")
        .last()
    ):
        messages.error(
            request, "You need a vessel to create a trip.", fail_silently=True
        )
        return redirect(reverse("vessels:vessel_setup"))
    return redirect(reverse("charter:new_trip_details", args=[vessel.id]))


@login_required
@admin_required
def new_trip_details(request: HttpRequest, vessel_id: int):
    try:
        vessel = Vessel.objects.get(id=vessel_id)
    except Vessel.DoesNotExist:
        messages.error("Vessel Does not exist", fail_silently=True)
    user: User = request.user
    notifications, new_notifications = get_admin_notifications(
        user.admin_profile,
    )
    if request.method == "POST":
        form = CharterDetailsForm(data=request.POST)
        if form.is_valid():
            embark_date = request.POST.get("embark_date")
            disembark_date = request.POST.get("disembark_date")
            suffix_number = auto_increment_booking_id()
            charter = create_charter_details(
                first_name=form.cleaned_data["first_name"].capitalize(),
                last_name=form.cleaned_data["last_name"].capitalize(),
                email=form.cleaned_data["email"],
                apa_budget=float(request.POST["apa_budget"].replace(",", "")),
                currency=request.POST["currency"],
                embark_city=form.cleaned_data["embark_city"].capitalize(),
                embark_country=form.cleaned_data["embark_country"].capitalize(),
                embark_date=datetime.strptime(embark_date, "%d %B %Y"),
                disembark_date=datetime.strptime(disembark_date, "%d %B %Y"),
                booking_id=f"{vessel.id}{vessel.name[:3].upper()}{suffix_number}",
                created_by=user,
                vessel=vessel,
            )
            return redirect(reverse("charter:charter_locations", args=[charter.id]))
    breadcrumbs = "Trip Details > Principal Info"
    notifications, new_notifications = get_admin_notifications(
        user.admin_profile,
    )
    ctx = {
        "active": "trips",
        "breadcrumbs": breadcrumbs,
        "notifications": notifications,
        "new_notifications": new_notifications,
        "user": user,
    }
    form = CharterDetailsForm()
    ctx["form"] = form

    return render(request, "charter/charter_details.html", ctx)


@login_required
@admin_required
def add_charter_locations(request: HttpRequest, charter_id: int = None) -> HttpResponse:
    """
    Update charter with charter locations details.
    """
    breadcrumbs = "Add a Charter > Departure & Arrival Locations"

    user: User = request.user

    charter = get_object_or_404(Charter, id=charter_id)

    principal_guest = charter.principal_guest
    notifications, new_notifications = get_admin_notifications(
        user.admin_profile,
    )

    ctx = {
        "active": "trips",
        "breadcrumbs": breadcrumbs,
        "user": user,
        "charter": charter,
        "vessel": charter.vessel,
        "principal_guest": principal_guest,
        "embark_date": charter.embark_date.strftime("%d %B %Y")
        if charter.embark_date
        else None,
        "notifications": notifications,
        "new_notifications": new_notifications,
        "disembark_date": charter.disembark_date.strftime("%d %B %Y")
        if charter.disembark_date
        else None,
    }

    if request.method == "POST":
        form = CharterLocationsForm(data=request.POST)
        if form.is_valid():
            update_charter_locations(
                charter=charter,
                # **form.cleaned_data,
                embark_name_of_dock=request.POST["embark_name_of_dock"].capitalize(),
                embark_city=request.POST["embark_city"].capitalize(),
                embark_country=request.POST["embark_country"].capitalize(),
                embark_additional_info=request.POST["embark_additional_info"],
                embark_date=datetime.strptime(request.POST["embark_date"], "%d %B %Y"),
                embark_time=form.cleaned_data["embark_time"],
                disembark_name_of_dock=request.POST[
                    "disembark_name_of_dock"
                ].capitalize(),
                disembark_city=request.POST["disembark_city"].capitalize(),
                disembark_country=request.POST["disembark_country"].capitalize(),
                disembark_additional_info=request.POST["disembark_additional_info"],
                disembark_date=datetime.strptime(
                    request.POST["disembark_date"], "%d %B %Y"
                ),
                disembark_time=form.cleaned_data["disembark_time"],
            )
            return redirect(reverse("charter:add_guests", args=[charter_id]))
    else:
        form = CharterLocationsForm()
        if charter.embark_name_of_dock:
            form = CharterLocationsForm(
                initial={
                    "embark_name_of_dock": charter.embark_name_of_dock,
                    "embark_city": charter.embark_city,
                    "embark_country": charter.embark_country,
                    "embark_time": charter.embark_time,
                    "disembark_name_of_dock": charter.embark_name_of_dock,
                    "disembark_city": charter.disembark_city,
                    "disembark_country": charter.disembark_country,
                    "disembark_time": charter.disembark_time,
                }
            )
            ctx["embark_additional_info"] = charter.embark_additional_info
            ctx["embark_date"] = charter.embark_date.strftime("%d %B %Y")
            ctx["embark_time"] = charter.embark_time
            ctx["disembark_additional_info"] = charter.embark_additional_info
            ctx["disembark_date"] = charter.disembark_date.strftime("%d %B %Y")
            ctx["disembark_time"] = charter.disembark_time

    ctx["form"] = form

    return render(request, "charter/charter_locations.html", ctx)


@login_required
@admin_required
def add_guests(request: HttpRequest, charter_id: int = None) -> HttpResponse:
    """
    Adding of guests
    """
    breadcrumbs = "Add a Charter > Invite Guests"

    user: User = request.user

    charter: Charter = get_object_or_404(Charter, id=charter_id)
    notifications, new_notifications = get_admin_notifications(
        user.admin_profile,
    )

    ctx = {
        "active": "trips",
        "breadcrumbs": breadcrumbs,
        "user": user,
        "charter": charter,
        "vessel": charter.vessel,
        "notifications": notifications,
        "new_notifications": new_notifications,
        "principal_guest": charter.principal_guest,
    }

    if request.method == "POST":
        form = AddGuestsForm(
            data=request.POST,
            charter=charter,
            added_guest_count=charter.guests.all().count(),
        )
        if form.is_valid():
            # Add guests
            emails = request.POST.getlist("guest_email", "")
            valid_emails, invalid_emails = check_emails(emails)
            removable_guests: QuerySet[GuestDetail] = charter.guests.filter(
                profile__isnull=True
            )
            charter.guests.clear()
            removable_guests.delete()
            for email in valid_emails:
                guest_user = User.objects.filter(email=email)
                if valid_emails.count(email) > 1:
                    messages.error(
                        request, "Guest list must not have duplicate emails."
                    )
                    return redirect(reverse("charter:add_guests", args=[charter_id]))
                elif guest_user.exists() and charter.principal_guest.email == email:
                    messages.error(
                        request, f"Invalid email: {email} is the principal guest."
                    )
                    return redirect(reverse("charter:add_guests", args=[charter_id]))
                elif guest_user.exists() and guest_user.last().is_admin:
                    messages.error(request, f"Invalid email: {email} is an admin.")
                    return redirect(reverse("charter:add_guests", args=[charter_id]))
                else:
                    if email != "":
                        add_guests_email(
                            charter=charter,
                            email=email,
                        )
            if invalid_emails:
                messages.error(
                    request,
                    f"Invalid emails ({', '.join(invalid_emails)}) were not included in the guests.",
                )
                return redirect(reverse("charter:add_guests", args=[charter_id]))
            return redirect(reverse("charter:review_and_submit", args=[charter_id]))
    else:
        form = AddGuestsForm(
            charter=charter, added_guest_count=charter.guests.all().count()
        )
        if charter:
            initial_fields = {}
            form = AddGuestsForm(
                initial=initial_fields,
                charter=charter,
                added_guest_count=charter.guests.all().count(),
            )

    ctx["form"] = form

    return render(request, "charter/add_guests.html", ctx)


@login_required
@admin_required
def review_and_submit(request: HttpRequest, charter_id: int = None) -> HttpResponse:
    """
    Display all charter details and list of guests
    """
    breadcrumbs = "Add a Charter > Review and Submit"

    user: User = request.user

    charter = get_object_or_None(Charter, id=charter_id)

    ctx = {
        "active": "trips",
        "breadcrumbs": breadcrumbs,
        "user": user,
        "vessel": charter.vessel,
        "charter": charter,
        "guests": charter.guests.all().order_by("first_name"),
        "principal_guest": charter.principal_guest,
    }

    return render(request, "charter/review_and_submit.html", ctx)


@login_required
@admin_required
def charter_success(request: HttpRequest, charter_id: int = None) -> HttpResponse:
    """
    Overview of charter
    """
    title = "Success"

    user: User = request.user

    charter = get_object_or_None(Charter, id=charter_id)
    notifications, new_notifications = get_admin_notifications(
        user.admin_profile,
    )

    ctx = {
        "title": title,
        "user": user,
        "vessel": charter.vessel,
        "charter": charter,
        "notifications": notifications,
        "new_notifications": new_notifications,
        "principal_guest": charter.principal_guest,
    }

    complete_charter_setup(charter=charter, is_complete=True)

    # Send email invite
    emails = list(charter.guests.values_list("email", flat=True))
    emails.append(charter.principal_guest.email)

    send_email_template(
        subject=charter.vessel.proper_name,
        recipients=list(emails),
        template="charter/email/trip_invite_new.html",
        data=ctx,
        is_secure=request.is_secure(),
    )

    return render(request, "charter/success.html", ctx)


@login_required
@admin_required
def guests(request: HttpRequest, charter_id: int) -> HttpResponse:
    """
    Display a charter's list of guests
    """
    user: User = request.user
    charter = get_object_or_404(Charter, id=charter_id)
    guest_list = list(charter.guests.all().order_by("id"))
    if charter.principal_guest not in guest_list:
        guest_list.insert(0, charter.principal_guest)

    notifications, new_notifications = get_admin_notifications(
        user.admin_profile,
    )
    ctx = {
        "user": user,
        "is_admin": user.admin_profile.is_admin,
        "charter": charter,
        "breadcrumbs": f"Dashboard > Itinerary > {charter}",
        "active": "guests",
        "vessel": charter.vessel,
        "guests": guest_list,
        "principal_guest": charter.principal_guest,
        "notifications": notifications,
        "new_notifications": new_notifications,
        "guests_email": list(guest.email for guest in guest_list),
    }

    if request.method == "POST":
        form = AddGuestForm(data=request.POST, charter=charter)
        if form.is_valid():
            email = request.POST.get("email", "")
            if charter.guests.filter(email=email).exists():
                messages.error(request, f"Guest {email} already exists.")
            else:
                add_guests_email(
                    charter=charter,
                    email=email,
                )
                emails = []
                emails.append(email)

                template = None
                subject = None
                current_date: date = timezone.now().date()
                # Active or Upcoming Charters
                if (
                    charter.embark_date <= current_date <= charter.disembark_date
                ) or charter.embark_date >= current_date:
                    subject = f"Welcome Aboard {charter.vessel.proper_name}!"
                    template = "charter/email/trip_invite_new.html"
                # Past Charters
                else:
                    # Unregistered guests will receive an email to register
                    if charter.guests.filter(email=email).last().profile is None:
                        subject = f"We hope you enjoyed your trip aboard {charter.vessel.proper_name}!"
                        template = "charter/email/trip_invite_reminder.html"
                    # Registered guests
                    else:
                        return redirect(reverse("charter:guests", args=[charter_id]))

                send_email_template(
                    subject=subject,
                    recipients=list(emails),
                    template=template,
                    data=ctx,
                    is_secure=request.is_secure(),
                )

            return redirect(reverse("charter:guests", args=[charter_id]))
    else:
        form = AddGuestForm(charter=charter)

    ctx["form"] = form

    if request.method == "POST":
        response = generate_trip_details_pdf(request, charter)
        return response

    return render(request, "charter/guests.html", ctx)


@login_required
@admin_required
def preferences_and_shopping_list(
    request: HttpRequest, charter_id: int
) -> HttpResponse:
    """
    Display a charter's summary of preferences and shopping list.
    """
    charter = get_object_or_404(Charter, id=charter_id)
    ctx = {
        "charter": charter,
        "breadcrumbs": f"Dashboard > Itinerary > {charter}",
        "active": "preferences_and_shopping_list",
        "notifications": get_admin_notifications(request.user.admin_profile),
        "vessel": charter.vessel,
    }
    ctx["form"] = PreferencesShoppingListForm(charter=charter)

    if request.method == "POST":
        form = PreferencesShoppingListForm(data=request.POST, charter=charter)
        if not form.is_valid() or len(request.POST.getlist("pref_shopping_list")) < 1:
            messages.error(request, "No Preference Selected.")
        elif form.is_valid():

            return get_shopping_list_response(
                request,
                charter,
                preference_list=form.data.getlist("pref_shopping_list"),
            )

    return render(request, "charter/preferences_and_shopping_list.html", ctx)


@login_required
@admin_required
def guest_details(request: HttpRequest, charter_id: int, guest_id: int) -> HttpResponse:
    """
    Display a specific guest's details
    """
    guest = get_object_or_404(GuestDetail, pk=guest_id)
    charter = Charter.objects.get(pk=charter_id)

    ctx = {
        "guest": guest,
        "charter": charter,
        "breadcrumbs": f"Dashboard > Itinerary > {charter}",
        "notifications": get_admin_notifications(request.user.admin_profile),
        "vessel": charter.vessel,
        # "is_admin": request.user.admin_profile.is_admin,
        "is_admin": request.user.admin_profile.is_admin,
    }

    if request.method == "POST":
        response = generate_guest_details_pdf(request, guest, charter)
        return response

    return render(request, "charter/guest_details.html", ctx)


@login_required
@admin_required
def guest_food_preferences(
    request: HttpRequest, charter_id: int, guest_id: int
) -> HttpResponse:
    """
    Display a specific guest's food preferences
    """
    guest = get_object_or_404(GuestDetail, pk=guest_id)
    charter = Charter.objects.get(pk=charter_id)

    ctx = {
        "guest": guest,
        "charter": charter,
        "breadcrumbs": f"Dashboard > Itinerary > {charter}",
        "notifications": get_admin_notifications(request.user.admin_profile),
        "vessel": charter.vessel,
    }

    if request.method == "POST":
        response = generate_guest_details_pdf(request, guest, charter)
        return response

    return render(request, "charter/guest_food_preferences.html", ctx)


@login_required
@admin_required
def guest_meal_and_room_preferences(
    request: HttpRequest, charter_id: int, guest_id: int
) -> HttpResponse:
    """
    Display a specific guest's meal and room preferences
    """
    guest = get_object_or_404(GuestDetail, pk=guest_id)
    charter = Charter.objects.get(pk=charter_id)

    breakfast_selection = None
    lunch_selection = None
    dinner_selection = None
    meal_and_room_preferences = (
        guest.meal_and_room_preferences
        if hasattr(guest, "meal_and_room_preferences")
        else None
    )
    if meal_and_room_preferences:
        breakfast_selection = meal_and_room_preferences.breakfast_selection
        lunch_selection = meal_and_room_preferences.lunch_selection
        dinner_selection = meal_and_room_preferences.dinner_selection

    ctx = {
        "guest": guest,
        "charter": charter,
        "breadcrumbs": f"Dashboard > Itinerary > {charter}",
        "vessel": charter.vessel,
        "notifications": get_admin_notifications(request.user.admin_profile),
        "breakfast_selection": breakfast_selection.name
        if hasattr(breakfast_selection, "name")
        else None,
        "lunch_selection": lunch_selection.name
        if hasattr(lunch_selection, "name")
        else None,
        "dinner_selection": dinner_selection.name
        if hasattr(dinner_selection, "name")
        else None,
    }

    if request.method == "POST":
        response = generate_guest_details_pdf(request, guest, charter)
        return response

    return render(request, "charter/guest_meal_and_room_preferences.html", ctx)


@login_required
@admin_required
def guest_diet_services_sizing(
    request: HttpRequest, charter_id: int, guest_id: int
) -> HttpResponse:
    """
    Display a specific guest's meal and room preferences
    """
    guest = get_object_or_404(GuestDetail, pk=guest_id)
    charter = Charter.objects.get(pk=charter_id)

    other_services = None

    diet_services_sizes_preferences = (
        guest.diet_services_sizes_preferences
        if hasattr(guest, "diet_services_sizes_preferences")
        else None
    )

    if diet_services_sizes_preferences:
        other_services = (
            diet_services_sizes_preferences.other_service
            if hasattr(diet_services_sizes_preferences, "other_service")
            else None
        )

    ctx = {
        "guest": guest,
        "charter": charter,
        "breadcrumbs": f"Dashboard > Itinerary > {charter}",
        "vessel": charter.vessel,
        "notifications": get_admin_notifications(request.user.admin_profile),
        "other_services": other_services.name
        if hasattr(other_services, "name")
        else None,
    }

    if request.method == "POST":
        response = generate_guest_details_pdf(request, guest, charter)
        return response

    return render(request, "charter/guest_diet_services_sizing.html", ctx)


@login_required
@admin_required
def guest_beverage_alcohol(
    request: HttpRequest, charter_id: int, guest_id: int
) -> HttpResponse:
    """
    Display a specific guest's beverage and alcohol preferences
    """
    guest = get_object_or_404(GuestDetail, pk=guest_id)
    charter = Charter.objects.get(pk=charter_id)

    beverages_and_alcoholic_preferences = (
        guest.beverages_and_alcoholic_preferences
        if hasattr(guest, "beverages_and_alcoholic_preferences")
        else None
    )
    milk_selection = None
    coffee_selection = None
    tea_selection = None
    water_selection = None
    juice_selection = None
    sodas_and_mixers_selection = None
    add_ons_selection = None

    if beverages_and_alcoholic_preferences:
        milk_selection = beverages_and_alcoholic_preferences.milk_selection
        coffee_selection = beverages_and_alcoholic_preferences.coffee_selection
        tea_selection = beverages_and_alcoholic_preferences.tea_selection
        water_selection = beverages_and_alcoholic_preferences.water_selection
        juice_selection = beverages_and_alcoholic_preferences.juice_selection
        sodas_and_mixers_selection = (
            beverages_and_alcoholic_preferences.sodas_and_mixers_selection
        )
        add_ons_selection = beverages_and_alcoholic_preferences.add_ons_selection

    ctx = {
        "guest": guest,
        "charter": charter,
        "breadcrumbs": f"Dashboard > Itinerary > {charter}",
        "vessel": charter.vessel,
        "notifications": get_admin_notifications(request.user.admin_profile),
        "milk_selection": milk_selection.name
        if hasattr(milk_selection, "name")
        else None,
        "coffee_selection": coffee_selection.name
        if hasattr(coffee_selection, "name")
        else None,
        "tea_selection": tea_selection.name if hasattr(tea_selection, "name") else None,
        "water_selection": water_selection.name
        if hasattr(water_selection, "name")
        else None,
        "juice_selection": juice_selection.name
        if hasattr(juice_selection, "name")
        else None,
        "sodas_and_mixers_selection": sodas_and_mixers_selection.name
        if hasattr(sodas_and_mixers_selection, "name")
        else None,
        "add_ons_selection": add_ons_selection.name
        if hasattr(add_ons_selection, "name")
        else None,
    }

    if request.method == "POST":
        response = generate_guest_details_pdf(request, guest, charter)
        return response

    return render(request, "charter/guest_beverage_alcohol.html", ctx)


@login_required
@admin_required
def trip_details(request: HttpRequest, charter_id: int) -> HttpResponse:
    charter: Charter = get_object_or_404(
        Charter,
        id=charter_id,
    )
    try:
        is_admin = request.user.admin_profile.is_admin
    except Exception as err:
        print(err)
        is_admin = False

    if not charter.principal_guest:
        messages.warning(request, "This charter has no principal guest.")
        return redirect(
            reverse("charter:charter_details", args=[charter.vessel.id, charter.id])
        )

    breadcrumbs = f"Dashboard > Itinerary > {charter}"
    ctx = {
        "charter": charter,
        "principal": charter.principal_guest,
        "active": "trip_details",
        "notifications": get_admin_notifications(request.user.admin_profile),
        "breadcrumbs": breadcrumbs,
        "vessel": charter.vessel,
        "is_admin": is_admin,
    }

    if request.method == "POST":
        response = generate_trip_details_pdf(request, charter)
        return response

    return render(request, "charter/trip_details.html", ctx)


@login_required
@guest_required
def all_trips(request: HttpRequest) -> HttpResponse:

    user: User = request.user

    guest = user.guest_details
    if guest.is_principal:
        charters = guest.principal_charters.all()
    else:
        charters = Charter.objects.filter(
            guests__email=user.email, is_complete=True
        ).all()

    notifications, new_notifications = get_admin_notifications(
        user.admin_profile,
    )

    ctx = {
        "title": "Trips",
        "charters": charters,
        "guest": guest,
        "notifications": notifications,
        "new_notifications": new_notifications,
    }

    return render(request, "charter/guests/all_trips.html", ctx)


@login_required
@guest_required
def guest_trip_details(request: HttpRequest, charter_id: int) -> HttpResponse:

    charter: Charter = get_object_or_404(
        Charter,
        id=charter_id,
    )
    ctx = {
        "title": "Trips",
        "charter": charter,
        "notifications": get_admin_notifications(request.user.admin_profile),
    }

    return render(request, "charter/guests/guest_trip_details.html", ctx)


@login_required
@admin_required
def delete_guest(request: HttpRequest, charter_id: int, guest_id: int) -> HttpResponse:
    """
    Delete specific guest of a charter
    """
    # charter = get_object_or_404(Charter, pk=charter_id)

    # guest = charter.guests.filter(pk=guest_id).last()
    # charter.guests.filter(id=guest_id).delete()
    guest = get_object_or_404(GuestDetail, pk=guest_id)
    charter = guest.charters.filter(pk=charter_id).last()
    guest.charters.remove(charter)

    ctx = {
        "charter": charter,
        "breadcrumbs": f"Dashboard > Itinerary > {charter}",
        "active": "guests",
        "notifications": get_admin_notifications(request.user.admin_profile),
    }
    messages.error(request, f"Guest {guest} has been deleted.")
    form = AddGuestForm(charter=charter)

    ctx["form"] = form
    return redirect(reverse("charter:guests", args=[charter.pk]))


@login_required
@admin_required
def edit_trip_details(request: HttpRequest, charter_id: int = None) -> HttpResponse:
    """
    Update charter with charter locations details.
    """
    breadcrumbs = "Update Charter > Departure & Arrival Locations"

    user: User = request.user

    charter = get_object_or_404(Charter, id=charter_id)

    principal_guest = charter.principal_guest
    notifications, new_notifications = get_admin_notifications(
        user.admin_profile,
    )

    ctx = {
        "active": "trips",
        "breadcrumbs": breadcrumbs,
        "user": user,
        "charter": charter,
        "vessel": charter.vessel,
        "principal_guest": principal_guest,
        "embark_date": charter.embark_date.strftime("%d %B %Y"),
        "notifications": notifications,
        "new_notifications": new_notifications,
        "disembark_date": charter.disembark_date.strftime("%d %B %Y"),
    }
    if request.method == "POST":
        form = EditTripDetailsForm(data=request.POST)
        if form.is_valid():
            update_trip_details(
                charter=charter,
                first_name=form.cleaned_data["first_name"].capitalize(),
                last_name=form.cleaned_data["last_name"].capitalize(),
                email=form.cleaned_data["email"],
                apa_budget=float(request.POST["apa_budget"].replace(",", "")),
                currency=request.POST["currency"],
                embark_name_of_dock=request.POST["embark_name_of_dock"].capitalize(),
                embark_city=request.POST["embark_city"].capitalize(),
                embark_country=request.POST["embark_country"].capitalize(),
                embark_additional_info=request.POST["embark_additional_info"],
                embark_date=ps.parse(request.POST["embark_date"]),
                embark_time=form.cleaned_data["embark_time"],
                disembark_name_of_dock=request.POST[
                    "disembark_name_of_dock"
                ].capitalize(),
                disembark_city=request.POST["disembark_city"].capitalize(),
                disembark_country=request.POST["disembark_country"].capitalize(),
                disembark_additional_info=request.POST["disembark_additional_info"],
                disembark_date=ps.parse(request.POST["disembark_date"]),
                disembark_time=form.cleaned_data["disembark_time"],
            )
            messages.success(request, "Trip Details have been successfully updated.")
            return redirect(reverse("charter:trip_details", args=[charter_id]))
    else:
        form = EditTripDetailsForm()
        if charter.embark_name_of_dock:
            form = EditTripDetailsForm(
                initial={
                    "first_name": charter.principal_guest.first_name,
                    "last_name": charter.principal_guest.last_name,
                    "email": charter.principal_guest.email,
                    "embark_name_of_dock": charter.embark_name_of_dock,
                    "embark_city": charter.embark_city,
                    "embark_country": charter.embark_country,
                    "disembark_name_of_dock": charter.embark_name_of_dock,
                    "disembark_city": charter.disembark_city,
                    "disembark_country": charter.disembark_country,
                }
            )
            ctx["apa_budget"] = "{:,.2f}".format(charter.apa_budget)
            ctx["currency"] = charter.currency
            ctx["embark_additional_info"] = charter.embark_additional_info
            ctx["embark_date"] = charter.embark_date.strftime("%d %B %Y")
            ctx["embark_time"] = charter.embark_time
            ctx["disembark_additional_info"] = charter.embark_additional_info
            ctx["disembark_date"] = charter.disembark_date.strftime("%d %B %Y")
            ctx["disembark_time"] = charter.disembark_time

    ctx["form"] = form

    return render(request, "charter/trip_details_edit.html", ctx)


@login_required
@admin_required
def download_meal_times_and_types(
    request: HttpRequest, charter_id: int
) -> HttpResponse:
    """
    Download Meal Times and Types as PDF.
    """
    charter = get_object_or_404(Charter, id=charter_id)

    breakfast_selection = []
    lunch_selection = []
    dinner_selection = []
    meal_and_room_preferences = (
        charter.principal_guest.meal_and_room_preferences
        if hasattr(charter.principal_guest, "meal_and_room_preferences")
        else []
    )
    if meal_and_room_preferences:
        breakfast_selection = meal_and_room_preferences.breakfast_selection.name or ""
        lunch_selection = meal_and_room_preferences.lunch_selection.name or ""
        dinner_selection = meal_and_room_preferences.dinner_selection.name or ""
    ctx = {
        "charter": charter,
        "principal": charter.principal_guest,
        "notifications": get_admin_notifications(request.user.admin_profile),
        "breakfast_selection": breakfast_selection,
        "lunch_selection": lunch_selection,
        "dinner_selection": dinner_selection,
    }

    response = generate_meal_times_and_types_pdf(request, ctx)
    return response


@login_required
@admin_required
def download_shopping_list(
    request: HttpRequest,
    charter_id: int,
) -> HttpResponse:
    origin = request.META.get("HTTP_REFERER", reverse("admins:dashboard"))

    try:
        charter: Charter = Charter.objects.get(id=charter_id)
    except Charter.DoesNotExist:
        return redirect(origin)

    return get_shopping_list_response(request, charter)
