from django.utils import timezone

from django.contrib import messages
from django.contrib.auth import login as base_login, logout as base_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from authentication.decorators import anonymous_required, guest_required
from authentication.forms import LoginForm
from authentication.models import User
from authentication.services import send_password_reset_code, change_user_password
from charter.models import Charter, GuestDetail
from core.models import Document
from guests.forms import (
    ForgotPasswordForm,
    ConfirmForgotPasswordCodeForm,
    ChangePasswordForm,
    DocumentForm,
    PrincipleOnboardingForm,
    ProfileImageForm,
    RegistrationForm,
    SettingsChangePasswordForm,
)
from guests.services import (
    create_guest_account,
    create_guest_detail,
    update_guest_detail_on_register,
    update_guest_detail,
)
from preferences.forms import (
    BeveragesAlcoholPreferencesForm,
    DietServicesSizesForm,
    FoodPreferencesForm,
    MealAndRoomPreferencesForm,
)
from preferences.helpers import get_max_pref_created_date, get_additional_alcohol
from preferences.services import (
    create_beverages_alcohol_preferences,
    create_diet_services_sizes_preferences,
    create_food_preferences,
    create_meal_and_room_preferences,
    update_beverages_alcohol_preferences,
    update_diet_services_sizes_preferences,
    update_food_preferences,
    update_meal_and_room_preferences,
)


@login_required
@guest_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Version 2 for guest dashboard
    """
    user: User = request.user
    guest = user.guest_details

    ctx = {
        "user": user,
        "guest": guest,
    }

    return render(request, "guests/ver2/dashboard.html", ctx)


@login_required
@guest_required
def trips(request: HttpRequest) -> HttpResponse:
    """
    Version 2 for guest trips
    """

    return render(request, "guests/ver2/trips.html", {})
