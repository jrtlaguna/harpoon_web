from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as base_login
from django.contrib.auth import logout as base_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from admins.forms import (
    ChangePasswordForm,
    ConfirmForgotPasswordCodeForm,
    CrewProfileForm,
    CrewProfileImageForm,
    ForgotPasswordForm,
    GuestInfoForm,
    GuestInfoProfileImageForm,
    RegistrationForm,
    SettingsChangePasswordForm,
    SettingsForm,
)
from admins.models import AdminProfile, CrewProfile, GuestInformation
from admins.services import (
    create_admin_account,
    create_crew_profile,
    create_guest_info,
    edit_crew_profile,
    edit_guest_info,
    update_admin_settings,
)
from admins.utils import get_admin_notifications
from authentication.decorators import admin_required, anonymous_required
from authentication.forms import LoginForm
from authentication.models import User
from authentication.services import change_user_password, send_password_reset_code
from charter.helpers import get_crew_profile_response
from charter.models import Charter, GuestDetail
from guests.forms import ProfileImageForm


@anonymous_required
def login(request: HttpRequest) -> HttpResponse:
    """
    Authenticates and logs in an admin.
    """
    if request.method == "POST":
        form = LoginForm(data=request.POST, form_action="admins:login")
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["username"],
                password=request.POST["password"],
            )

            if not user.is_admin:
                messages.error(
                    request, "You need to be an admin to perform this action."
                )
                return redirect(request.META.get("HTTP_REFERER"))

            else:
                base_login(request, user)
                messages.success(request, "You have been logged in.")
                return redirect(reverse("admins:dashboard"))
    else:
        form = LoginForm(form_action="admins:login")

    ctx = {
        "form": form,
    }

    return render(request, "admins/login.html", ctx)


@login_required
def logout(request: HttpRequest) -> HttpResponse:
    """
    Logs an admin out of the system.
    """
    base_logout(request)
    messages.error(request, "You have been logged out.")
    return redirect(reverse("admins:login"))


@anonymous_required
def register(request: HttpRequest) -> HttpResponse:
    """
    Register a new admin account.
    """
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = create_admin_account(
                first_name=form.cleaned_data["first_name"].capitalize(),
                last_name=form.cleaned_data["last_name"].capitalize(),
                email=form.cleaned_data["email"],
                role=form.cleaned_data["role"],
                phone_number=form.cleaned_data["phone_number"],
                password=request.POST["password1"],
            )
            base_login(request, user)
            messages.success(request, "Your account is now created!")
            return redirect(reverse("vessels:vessel_setup"))
    else:
        form = RegistrationForm()

    ctx = {
        "form": form,
    }

    return render(request, "admins/registration.html", ctx)


@anonymous_required
def forgot_password(request: HttpRequest) -> HttpResponse:
    """
    Entry point for the forgot password flow.
    """
    if request.method == "POST":
        form = ForgotPasswordForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            send_password_reset_code(email=email)
            return redirect(reverse("admins:forgot_password_code", args=[email]))
    else:
        form = ForgotPasswordForm()

    ctx = {
        "form": form,
    }

    return render(request, "admins/forgot_password.html", ctx)


@anonymous_required
def forgot_password_code(request: HttpRequest, email: str) -> HttpResponse:
    """
    Accepts the entered data from the forgot_password view for further processing.
    """
    if request.method == "POST":
        form = ConfirmForgotPasswordCodeForm(data=request.POST, email=email)
        if form.is_valid():
            code = f"{form.cleaned_data['char1']}{form.cleaned_data['char2']}{form.cleaned_data['char3']}{form.cleaned_data['char4']}"
            return redirect(reverse("admins:change_password", args=[email, code]))
    else:
        form = ConfirmForgotPasswordCodeForm(email=email)

    ctx = {
        "email": email,
        "form": form,
    }

    return render(request, "admins/forgot_password_code.html", ctx)


@anonymous_required
def resend_password_code(request: HttpRequest, email: str) -> HttpResponse:
    """
    Resends a new password reset code.
    """
    send_password_reset_code(email=email)
    messages.info(request, "Password reset code re-sent.")
    return redirect(reverse("admins:forgot_password_code", args=[email]))


@anonymous_required
def change_password(request: HttpRequest, email: str, code: str) -> HttpResponse:
    """
    Last step of the forgot password flow that actually accepts a new password from the user.
    """
    user = request.user
    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST, email=email, code=code)
        if form.is_valid():
            change_user_password(email=email, password=form.cleaned_data["password"])
            messages.success(request, "Password successfully changed")
            return redirect(reverse("admins:login"))
    else:
        form = ChangePasswordForm(email=email, code=code)

    ctx = {
        "form": form,
        "user": user,
        "header_title": get_header_title(user.admin_profile),
    }
    return render(request, "admins/change_password.html", ctx)


@login_required
@admin_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Main admin dashboard
    """
    incomplete_charters_sort = request.GET.get("incomplete_charters_sort", "booking_id")
    active_charters_sort = request.GET.get("active_charters_sort", "booking_id")
    upcoming_sort = request.GET.get("upcoming_sort", "booking_id")
    past_charters_sort = request.GET.get("past_charters_sort", "booking_id")

    current_date: date = timezone.now().date()
    admin_profile: AdminProfile = request.user.admin_profile
    active_vessel = admin_profile.vessels.filter(is_active=True).first()
    if not active_vessel:
        return redirect(reverse("vessels:vessel_setup"))
    charters: QuerySet[Charter] = active_vessel.charters.all().order_by("-embark_date")
    incomplete_charters: QuerySet[Charter] = [
        charter
        for charter in charters.order_by(incomplete_charters_sort)
        if not charter.is_complete
    ]
    active_charters: QuerySet[Charter] = charters.filter(
        embark_date__lte=current_date,
        disembark_date__gte=current_date,
    ).order_by(active_charters_sort)
    upcoming = charters.filter(
        is_complete=True,
        embark_date__gt=current_date,
    ).order_by(upcoming_sort)
    past_charters = charters.filter(disembark_date__lt=current_date).order_by(
        past_charters_sort
    )
    notifications, new_notifications = get_admin_notifications(
        admin_profile,
    )
    ctx = {
        "incomplete_charters": incomplete_charters,
        "active_charters": active_charters,
        "upcoming_charters": upcoming,
        "past_charters": past_charters,
        "vessel": active_vessel,
        "admin": admin_profile,
        "user": request.user,
        "notifications": notifications,
        "new_notifications": new_notifications,
    }
    return render(request, "admins/dashboard.html", ctx)


def seen_notifications(request: HttpRequest) -> JsonResponse:
    from admins.utils import THREE_WEEKS_AGO

    user: User = request.user
    user.admin_profile.notifications.filter(updated_at__lte=THREE_WEEKS_AGO).update(
        seen=True
    )
    return JsonResponse({"message": "Success seen"})


@login_required
@admin_required
def settings(request: HttpRequest) -> HttpResponse:
    """
    Settings page for the admin.
    """
    admin: User = request.user
    image_form = ProfileImageForm(user=admin)
    initial = {
        "first_name": admin.first_name,
        "last_name": admin.last_name,
        "email": admin.email,
        "role": admin.admin_profile.role,
        "phone_number": admin.admin_profile.phone_number,
        "receive_email_notifications": admin.admin_profile.receive_email_notifications,
    }
    if request.method == "POST":
        form = SettingsForm(
            data=request.POST,
            initial=initial,
            admin=admin,
        )
        if form.is_valid():
            update_admin_settings(
                admin=admin,
                **form.cleaned_data,
            )
            messages.success(request, "Your settings has been updated.")
            return redirect(reverse("admins:dashboard"))
    else:
        form = SettingsForm(initial=initial, admin=admin)

    ctx = {
        "form": form,
        "active": "account_settings",
        "user": admin,
        "image_form": image_form,
        "notifications": get_admin_notifications(admin.admin_profile),
        "header_title": get_header_title(admin.admin_profile),
    }

    return render(request, "admins/settings.html", ctx)


@login_required
@admin_required
def settings_change_password(request: HttpRequest) -> HttpResponse:
    """
    Change password form inside the admin dashboard.
    """
    admin: User = request.user

    if request.method == "POST":
        form = SettingsChangePasswordForm(
            data=request.POST,
            admin=admin,
        )
        if form.is_valid():
            change_user_password(
                email=admin.email, password=form.cleaned_data["password1"]
            )
            base_logout(request)
            messages.success(request, "Your password has been updated.")
            return redirect(reverse("admins:login"))
    else:
        form = SettingsChangePasswordForm(admin=admin)

    ctx = {
        "form": form,
        "active": "account_settings",
        "user": admin,
        "notifications": get_admin_notifications(admin.admin_profile),
        "header_title": get_header_title(admin.admin_profile),
    }

    return render(request, "admins/settings_change_password.html", ctx)


@login_required
@admin_required
def search(request: HttpRequest) -> HttpResponse:
    """
    Used to search data related to currently logged in admin
    """
    admin: AdminProfile = request.user.admin_profile
    if not (vessel := admin.vessels.filter(is_active=True).first()):
        return redirect(reverse("vessels:vessel_setup"))

    ctx = {
        "active": "search",
        "user": request.user,
        "notifications": get_admin_notifications(admin),
        "active_vessel": vessel,
    }
    if request.method == "POST":

        if keyword := request.POST.get("keyword"):
            vessel_ids = list(admin.vessels.values_list("id", flat=True))
            charters = Charter.objects.filter(vessel__id__in=vessel_ids)
            guests = GuestDetail.objects.filter(
                Q(charters__id__in=charters.values_list("id", flat=True)),
                (
                    Q(first_name__icontains=keyword)
                    | Q(last_name__icontains=keyword)
                    | Q(email__icontains=keyword)
                ),
            )
            charters = charters.filter(
                (
                    Q(principal_guest__first_name__icontains=keyword)
                    | Q(principal_guest__last_name__icontains=keyword)
                ),
            )
            ctx["result"] = []

            guest_urls = [
                {
                    "url": reverse("admins:guest_search", args=[guest.id]),
                    "name": f"{guest.__str__()} / Guest",
                }
                for guest in guests
            ]

            charter_urls = [
                {
                    "url": reverse("charter:charter_details", args=[charter.id]),
                    "name": f"{charter.__str__()} / Charter",
                }
                for charter in charters
            ]

            ctx["result"] += guest_urls
            ctx["result"] += charter_urls

        return render(request, "admins/partials/search_results.html", ctx)
    return render(request, "admins/search.html", ctx)


@login_required
@admin_required
def guest_search(request: HttpRequest, guest_id: int) -> HttpResponse:
    try:
        guest_detail = GuestDetail.objects.get(id=guest_id)
        charter_id = guest_detail.charters.last().id
        return redirect(
            reverse(
                "charter:guest_details",
                args=[
                    charter_id,
                    guest_detail.id,
                ],
            )
        )
    except GuestDetail.DoesNotExist:
        pass
        # return redirect(reverse("admins:search"))
    return redirect(reverse("admins:search"))


def get_header_title(profile):
    return profile.vessels.filter(is_active=True).first().proper_name


def privacy_policy(request: HttpRequest) -> HttpResponse:
    ctx = {
        "user": request.user,
        "admin": request.user.admin_profile,
        "page_name": "Privacy Policy",
    }
    return render(request, "admins/privacy_policy.html", ctx)


def terms_and_conditions(request: HttpRequest) -> HttpResponse:
    ctx = {
        "user": request.user,
        "admin": request.user.admin_profile,
        "page_name": "Terms and Conditions",
    }
    return render(request, "admins/terms_and_conditions.html", ctx)


def add_previous_yacht(request: HttpRequest) -> HttpResponse:
    from random import randint

    ctx = {
        "random_int": randint(1, 1000),
    }
    return render(request, "admins/partials/add_previous_yacht.html", ctx)


@login_required
@admin_required
def crew_profile_list(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    admin: AdminProfile = user.admin_profile
    if not (vessel := admin.vessels.filter(is_active=True).first()):
        return redirect(reverse("vessels:vessel_setup"))

    ctx = {
        "active": "crew",
        "user": request.user,
        "admin": admin,
        "vessel": vessel,
        "crew_members": admin.crew_members.all(),
        "header_title": get_header_title(admin),
    }
    return render(request, "admins/crew_list.html", ctx)


@login_required
@admin_required
def crew_profile_edit(request: HttpRequest, crew_id: int) -> HttpResponse:
    user: User = request.user
    admin: AdminProfile = user.admin_profile
    try:
        crew = CrewProfile.objects.get(id=crew_id)
    except CrewProfile.DoesNotExist:
        messages.error(request, "Crew Profile not found.")
        return redirect(reverse("admins:crew_profile_list"))

    if not (vessel := admin.vessels.filter(is_active=True).first()):
        return redirect(reverse("vessels:vessel_setup"))

    image_form = CrewProfileImageForm(crew=crew)

    if request.method == "POST":
        form = CrewProfileForm(data=request.POST)
        if form.is_valid():
            yacht_keys = [
                key for key in request.POST.keys() if key.startswith("previous_yacht")
            ]
            previous_yacht = [request.POST.get(key) for key in yacht_keys]
            edit_crew_profile(
                crew=crew,
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                crew_type=form.cleaned_data.get("crew_type"),
                previous_yacht=previous_yacht,
                interest=form.cleaned_data.get("interest"),
                about=form.cleaned_data.get("about"),
            )
            return redirect(reverse("admins:crew_profile_list"))
        else:
            messages.error(request, "Something Went Wrong.")

    form = CrewProfileForm(
        initial={
            "id": crew.id,
            "first_name": crew.first_name,
            "last_name": crew.last_name,
            "previous_yacht": crew.previous_yacht,
            "interest": crew.interest,
            "about": crew.about,
        },
    )

    ctx = {
        "active": "crew",
        "form": form,
        "image_form": image_form,
        "user": request.user,
        "crew": crew,
        "admin": admin,
        "vessel": vessel,
        "header_title": get_header_title(admin),
    }
    return render(request, "admins/edit_crew_profile.html", ctx)


@login_required
@admin_required
def crew_profile_create(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    admin: AdminProfile = user.admin_profile
    if not (vessel := admin.vessels.filter(is_active=True).first()):
        return redirect(reverse("vessels:vessel_setup"))

    if request.method == "POST":
        form = CrewProfileForm(data=request.POST)
        if form.is_valid():
            yacht_keys = [
                key for key in request.POST.keys() if key.startswith("previous_yacht")
            ]
            previous_yacht = [request.POST.get(key) for key in yacht_keys]
            create_crew_profile(
                admin=admin,
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                previous_yacht=previous_yacht,
                crew_type=form.cleaned_data.get("crew_type"),
                interest=form.cleaned_data.get("interest"),
                about=form.cleaned_data.get("about"),
            )
            return redirect(reverse("admins:crew_profile_list"))

    ctx = {
        "active": "crew",
        "user": request.user,
        "active_vessel": vessel,
        "form": CrewProfileForm(),
        "admin": admin,
        "vessel": vessel,
        "header_title": get_header_title(admin),
    }
    return render(request, "admins/create_crew_profile.html", ctx)


def crew_profile_image_upload(request: HttpRequest, crew_id: int) -> JsonResponse:
    try:
        crew = CrewProfile.objects.get(id=crew_id)
    except CrewProfile.DoesNotExist:
        messages.error(request, "Something went wrong")
        return redirect(reverse("admins:crew_profile_list"))
    image_form = CrewProfileImageForm(request.POST, request.FILES, crew=crew)
    if image_form.is_valid():
        crew.profile_picture.delete()
        crew.profile_picture = image_form.cleaned_data.get("profile_picture")
        crew.save()
        return JsonResponse({"url": crew.profile_picture.url})
    return JsonResponse({"error": "Please upload a valid image."})


def crew_profile_delete(request: HttpRequest, crew_id: int) -> JsonResponse:
    try:
        crew = CrewProfile.objects.get(id=crew_id)
    except CrewProfile.DoesNotExist:
        messages.error(request, "Something went wrong")
        return redirect(reverse("admins:crew_profile_list"))
    crew.delete()
    return JsonResponse({"message": "Success."})


def crew_profile_print(request: HttpRequest, crew_id: int) -> HttpResponse:
    try:
        crew = CrewProfile.objects.get(id=crew_id)
        response = get_crew_profile_response(request, crew)
        return response
    except CrewProfile.DoesNotExist:
        messages.error(request, "Something went wrong")
        return redirect(reverse("admins:crew_profile_list"))


@login_required
@admin_required
def guest_info_list(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    admin: AdminProfile = user.admin_profile
    if not (vessel := admin.vessels.filter(is_active=True).first()):
        return redirect(reverse("vessels:vessel_setup"))
    ctx = {
        "active": "guest_info",
        "user": request.user,
        "admin": admin,
        "vessel": vessel,
        "guest_info_list": admin.admin_guest_information.all(),
        "header_title": get_header_title(admin),
    }
    return render(request, "admins/guest_list.html", ctx)


@login_required
@admin_required
def guest_info_edit(request: HttpRequest, guest_info_id: int) -> HttpResponse:
    user: User = request.user
    admin: AdminProfile = user.admin_profile
    try:
        guest_info = GuestInformation.objects.get(id=guest_info_id)
    except GuestInformation.DoesNotExist:
        messages.error(request, "Guest Information not found.")
        return redirect(reverse("admins:guest_info_list"))

    if not (vessel := admin.vessels.filter(is_active=True).first()):
        return redirect(reverse("vessels:vessel_setup"))

    image_form = GuestInfoProfileImageForm(guest_info=guest_info)

    if request.method == "POST":
        form = GuestInfoForm(data=request.POST)
        if form.is_valid():
            date_of_birth = request.POST.get("date_of_birth")
            if date_of_birth:
                date_of_birth = datetime.strptime(date_of_birth, "%d %B %Y")
            edit_guest_info(
                guest_info=guest_info,
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                email=form.cleaned_data.get("email"),
                date_of_birth=date_of_birth,
                gender=form.cleaned_data.get("gender"),
                contact_number=form.cleaned_data.get("contact_number"),
                notes=form.cleaned_data.get("notes"),
                nationality=form.cleaned_data.get("nationality"),
            )
            return redirect(reverse("admins:guest_info_list"))
        else:
            messages.error(request, "Something Went Wrong.")

    form = GuestInfoForm(
        initial={
            "id": guest_info.id,
            "first_name": guest_info.first_name,
            "last_name": guest_info.last_name,
            "email": guest_info.email,
            "date_of_birth": guest_info.date_of_birth.strftime("%d %B %Y")
            if guest_info.date_of_birth
            else None,
            "gender": guest_info.gender,
            "contact_number": guest_info.contact_number,
            "notes": guest_info.notes,
            "nationality": guest_info.nationality,
        },
    )

    ctx = {
        "active": "guest_info",
        "form": form,
        "image_form": image_form,
        "user": request.user,
        "guest_info": guest_info,
        "admin": admin,
        "vessel": vessel,
        "header_title": get_header_title(admin),
    }
    return render(request, "admins/guest_edit.html", ctx)


@login_required
@admin_required
def guest_info_create(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    admin: AdminProfile = user.admin_profile
    if not (vessel := admin.vessels.filter(is_active=True).first()):
        return redirect(reverse("vessels:vessel_setup"))

    if request.method == "POST":
        form = GuestInfoForm(data=request.POST)
        date_of_birth = request.POST.get("date_of_birth")
        if date_of_birth:
            date_of_birth = datetime.strptime(date_of_birth, "%d %B %Y")
        if form.is_valid():
            create_guest_info(
                admin=admin,
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                email=form.cleaned_data.get("email"),
                gender=form.cleaned_data.get("gender"),
                contact_number=form.cleaned_data.get("contact_number"),
                date_of_birth=date_of_birth,
                nationality=form.cleaned_data.get("nationality"),
                notes=form.cleaned_data.get("notes"),
            )
            return redirect(reverse("admins:guest_info_list"))

    ctx = {
        "active": "guest_info",
        "user": request.user,
        "active_vessel": vessel,
        "form": GuestInfoForm(),
        "admin": admin,
        "vessel": vessel,
        "header_title": get_header_title(admin),
    }
    return render(request, "admins/guest_create.html", ctx)


def guest_info_image_upload(request: HttpRequest, guest_info_id: int) -> JsonResponse:
    try:
        guest_info = GuestInformation.objects.get(id=guest_info_id)
    except GuestInformation.DoesNotExist:
        messages.error(request, "Something went wrong")
        return redirect(reverse("admins:guest_info_list"))
    image_form = GuestInfoProfileImageForm(
        request.POST, request.FILES, guest_info=guest_info
    )
    if image_form.is_valid():
        guest_info.profile_picture.delete()
        guest_info.profile_picture = image_form.cleaned_data.get("profile_picture")
        guest_info.save()
        return JsonResponse({"url": guest_info.profile_picture.url})
    return JsonResponse({"error": "Please upload a valid image."})


def guest_info_delete(request: HttpRequest, guest_info_id: int) -> JsonResponse:
    try:
        guest_info = GuestInformation.objects.get(id=guest_info_id)
    except GuestInformation.DoesNotExist:
        messages.error(request, "Something went wrong")
        return redirect(reverse("admins:guest_info_list"))
    guest_info.delete()
    return JsonResponse({"message": "Success."})


def calendar(request: HttpRequest) -> HttpResponse:
    ctx = {
        "admin": request.user.admin_profile,
        "user": request.user,
    }
    return render(request, "admins/calendar.html", ctx)
