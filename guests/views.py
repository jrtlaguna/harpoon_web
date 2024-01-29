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


@anonymous_required
def login(request: HttpRequest) -> HttpResponse:
    """
    Authenticates and logs in a guest.
    """
    if request.method == "POST":
        form = LoginForm(data=request.POST, form_action="guests:login")
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )

            if not user.is_guest:
                messages.error(
                    request, "You need to be a guest to perform this action."
                )
            else:
                base_login(request, user)
                messages.success(request, "You have been logged in.")
                if hasattr(user, "guest_profile") and not hasattr(
                    user.guest_profile, "details"
                ):
                    return redirect(reverse("guests:profile_onboarding"))
                return redirect(reverse("guests:dashboard"))
    else:
        form = LoginForm(form_action="guests:login")

    ctx = {
        "form": form,
    }

    return render(request, "guests/login.html", ctx)


@login_required
def logout(request: HttpRequest) -> HttpResponse:
    """
    Logs a guest out of the system.
    """
    base_logout(request)
    messages.error(request, "You have been logged out.")
    return redirect(reverse("guests:login"))


@login_required
@guest_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Main guest dashboard
    """
    user: User = request.user

    current_date = timezone.now().date()
    guest = user.guest_details
    charters: QuerySet[Charter] = guest.charters.filter(
        is_complete=True, embark_date__gte=current_date
    ).order_by("embark_date")[:3]

    ctx = {
        "active": "dashboard",
        "title": "Dashboard",
        "user": user,
        "guest": guest,
        "pref_created_date": get_max_pref_created_date(guest),
        "upcoming_charters": charters,
    }
    return render(request, "guests/dashboard.html", ctx)


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
            return redirect(reverse("guests:forgot_password_code", args=[email]))
    else:
        form = ForgotPasswordForm()

    ctx = {
        "form": form,
    }

    return render(request, "guests/forgot_password.html", ctx)


@anonymous_required
def forgot_password_code(request: HttpRequest, email: str) -> HttpResponse:
    """
    Accepts the entered data from the forgot_password view for further processing.
    """
    if request.method == "POST":
        form = ConfirmForgotPasswordCodeForm(data=request.POST, email=email)
        if form.is_valid():
            code = f"{form.cleaned_data['char1']}{form.cleaned_data['char2']}{form.cleaned_data['char3']}{form.cleaned_data['char4']}"
            return redirect(reverse("guests:change_password", args=[email, code]))
    else:
        form = ConfirmForgotPasswordCodeForm(email=email)

    ctx = {
        "email": email,
        "form": form,
    }

    return render(request, "guests/forgot_password_code.html", ctx)


@anonymous_required
def resend_password_code(request: HttpRequest, email: str) -> HttpResponse:
    """
    Resends a new password reset code.
    """
    send_password_reset_code(email=email)
    messages.info(request, "Password reset code re-sent.")
    return redirect(reverse("guests:forgot_password_code", args=[email]))


@anonymous_required
def change_password(request: HttpRequest, email: str, code: str) -> HttpResponse:
    """
    Last step of the forgot password flow that actually accepts a new password from the user.
    """
    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST, email=email, code=code)
        if form.is_valid():
            change_user_password(email=email, password=form.cleaned_data["password"])
            messages.success(request, "Password successfully changed")
            return redirect(reverse("guests:login"))
    else:
        form = ChangePasswordForm(email=email, code=code)

    ctx = {
        "form": form,
    }
    return render(request, "guests/change_password.html", ctx)


@anonymous_required
def register(request: HttpRequest) -> HttpResponse:
    """
    Register a new guest account.
    """
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        # try:
        email = form.data.get("email")
        guest_details, _ = GuestDetail.objects.get_or_create(email=email)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"].capitalize()
            last_name = form.cleaned_data["last_name"].capitalize()

            user = create_guest_account(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=form.cleaned_data["phone_number"],
                password=form.cleaned_data["password1"],
            )

            base_login(request, user)
            update_guest_detail_on_register(
                user=user,
                guest_detail=guest_details,
                first_name=first_name,
                last_name=last_name,
            )
            messages.success(request, "Your account is now created!")
            charters = Charter.objects.filter(principal_guest=guest_details)
            for charter in charters:
                if guest_details not in charter.guests.all():
                    charter.guests.add(guest_details)
            if guest_details.principal_charters.exists():
                return redirect(reverse("guests:profile_onboarding"))
            return redirect(reverse("guests:dashboard"))
        # except GuestDetail.DoesNotExist:
        #     messages.error(
        #         request, f"{email} does not exist in the system. Please contact admin."
        #     )
        #     pass
    else:
        form = RegistrationForm()

    ctx = {
        "form": form,
    }

    return render(request, "guests/registration.html", ctx)


@login_required
@guest_required
def settings_change_password(request: HttpRequest) -> HttpResponse:
    """
    Change password form inside the guest dashboard.
    """
    guest: User = request.user
    title = "Security Settings"

    if request.method == "POST":
        form = SettingsChangePasswordForm(
            data=request.POST,
            guest=guest,
        )
        if form.is_valid():
            change_user_password(
                email=guest.email, password=form.cleaned_data["password1"]
            )
            if "email" in form.cleaned_data:
                guest.email = form.cleaned_data.get("email")
                guest.save()
            base_logout(request)
            messages.success(request, "Your password has been updated.")
            return redirect(reverse("guests:login"))
    else:
        form = SettingsChangePasswordForm(guest=guest)

    ctx = {"form": form, "active": "profile", "title": title}

    return render(request, "guests/settings_change_password.html", ctx)


@login_required
@guest_required
def onboarding_profile(request: HttpRequest) -> HttpResponse:
    """
    Principal onboarding
    """
    user: User = request.user
    template_name = "guests/onboarding/profile.html"
    image_form = ProfileImageForm(user=user)
    data = {}
    form = PrincipleOnboardingForm(view="profile_onboarding", user=user)
    if request.method == "POST":
        form = PrincipleOnboardingForm(
            request.POST, request.FILES, view="profile_onboarding", user=user
        )
        if form.is_valid():
            data = {
                "first_name": form.cleaned_data.get("first_name"),
                "last_name": form.cleaned_data.get("last_name"),
                "email": form.cleaned_data.get("email"),
                "phone_number": form.cleaned_data.get("phone_number"),
                "emergency_contact": form.cleaned_data.get("emergency_contact"),
                "emergency_relation": form.cleaned_data.get("emergency_relation"),
                "emergency_phone": form.cleaned_data.get("emergency_phone"),
                "address_street": form.cleaned_data.get("address_street"),
                "address_number": form.cleaned_data.get("address_number"),
                "address_city": form.cleaned_data.get("address_city"),
                "address_state": form.cleaned_data.get("address_state"),
                "address_zipcode": form.cleaned_data.get("address_zipcode"),
                "address_country": form.cleaned_data.get("address_country"),
                "medical_issues": form.cleaned_data.get("medical_issues"),
                "nationality": form.cleaned_data.get("nationality"),
                "passport": form.cleaned_data.get("passport"),
                "passport_number": form.cleaned_data.get("passport_number"),
                "passport_expiration": form.cleaned_data.get("passport_expiration"),
                "date_of_birth": form.cleaned_data.get("date_of_birth"),
                "allergies": form.cleaned_data.get("allergies"),
                "medications": form.cleaned_data.get("medications"),
                "salutation_nickname": form.cleaned_data.get("salutation_nickname"),
                "high_priority_details": form.cleaned_data.get("high_priority_details"),
                "lactose_intolerant": form.cleaned_data.get("lactose_intolerant"),
                "shellfish_allergy": form.cleaned_data.get("shellfish_allergy"),
                "nut_allergy": form.cleaned_data.get("nut_allergy"),
                "gluten_free": form.cleaned_data.get("gluten_free"),
                "none_food_sensitivity": form.cleaned_data.get("none_food_sensitivity"),
                "other": form.cleaned_data.get("other"),
                "other_notes": form.cleaned_data.get("other_notes"),
            }

            if not hasattr(user.guest_profile, "details"):
                create_guest_detail(
                    user=user,
                    **data,
                )
            else:
                update_guest_detail(
                    guest_detail=user.guest_profile.details,
                    **data,
                )
            return redirect(reverse("guests:yacht_food_onboarding"))
    else:
        initial = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        if hasattr(user, "guest_profile"):
            initial["phone_number"] = user.guest_profile.phone_number
            if hasattr(user.guest_profile, "details"):
                data = {
                    "emergency_contact": user.guest_profile.details.emergency_contact,
                    "emergency_relation": user.guest_profile.details.emergency_relation,
                    "emergency_phone": user.guest_profile.details.emergency_phone,
                    "address_street": user.guest_profile.details.address_street,
                    "address_number": user.guest_profile.details.address_number,
                    "address_city": user.guest_profile.details.address_city,
                    "address_state": user.guest_profile.details.address_state,
                    "address_zipcode": user.guest_profile.details.address_zipcode,
                    "address_country": user.guest_profile.details.address_country,
                    "nationality": user.guest_profile.details.nationality,
                    "passport_number": user.guest_profile.details.passport_number,
                    "passport": user.guest_profile.details.passport,
                    "passport_expiration": user.guest_profile.details.passport_expiration.strftime(
                        "%m/%d/%Y"
                    ),
                    "date_of_birth": user.guest_profile.details.date_of_birth.strftime(
                        "%m/%d/%Y"
                    ),
                    "medical_issues": user.guest_profile.details.medical_issues,
                    "allergies": user.guest_profile.details.allergies,
                    "medications": user.guest_profile.details.medications,
                    "salutation_nickname": user.guest_profile.details.salutation_nickname,
                    "high_priority_details": user.guest_profile.details.high_priority_details,
                    "lactose_intolerant": user.guest_profile.details.lactose_intolerant,
                    "shellfish_allergy": user.guest_profile.details.shellfish_allergy,
                    "nut_allergy": user.guest_profile.details.nut_allergy,
                    "gluten_free": user.guest_profile.details.gluten_free,
                    "none_food_sensitivity": user.guest_profile.details.none_food_sensitivity,
                    "other": user.guest_profile.details.other,
                    "other_notes": user.guest_profile.details.other_notes,
                }
        initial = {**initial, **data}
        form = PrincipleOnboardingForm(
            initial=initial, view="profile_onboarding", user=user
        )

    ctx = {"user": user, "form": form, "image_form": image_form}
    return render(request, template_name, ctx)


@login_required
@guest_required
def onboarding_yacht_food(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    guest_details = user.guest_profile.details
    form = FoodPreferencesForm(view="onboarding")
    food_preferences = (
        guest_details.food_preferences
        if hasattr(guest_details, "food_preferences")
        else None
    )
    if request.method == "POST":
        form = FoodPreferencesForm(data=request.POST, view="onboarding")
        if form.is_valid():
            if not food_preferences:
                food_preferences = create_food_preferences(
                    guest=guest_details,
                    general_cuisine=form.cleaned_data["general_cuisine"],
                    general_cuisine_notes=form.cleaned_data["general_cuisine_notes"],
                    fish_and_shellfish=form.cleaned_data["fish_and_shellfish"],
                    fish_and_shellfish_notes=form.cleaned_data[
                        "fish_and_shellfish_notes"
                    ],
                    meat=form.cleaned_data["meat"],
                    meat_notes=form.cleaned_data["meat_notes"],
                    bread=form.cleaned_data["bread"],
                    bread_notes=form.cleaned_data["bread_notes"],
                    salad=form.cleaned_data["salad"],
                    salad_notes=form.cleaned_data["salad_notes"],
                    soup=form.cleaned_data["soup"],
                    soup_notes=form.cleaned_data["soup_notes"],
                    cheese=form.cleaned_data["cheese"],
                    cheese_notes=form.cleaned_data["cheese_notes"],
                    dessert=form.cleaned_data["dessert"],
                    dessert_notes=form.cleaned_data["dessert_notes"],
                    kids_meals=form.cleaned_data.get("kids_meals"),
                    kids_allergies=form.cleaned_data.get("kids_allergies"),
                    kids_meals_notes=form.cleaned_data.get("kids_meals_notes"),
                )
            else:
                update_food_preferences(
                    food_preferences=food_preferences, **form.cleaned_data
                )
            return redirect(
                reverse(
                    "guests:onboarding_meals_and_room",
                )
            )
    else:
        if food_preferences:
            form = FoodPreferencesForm(
                initial={
                    "general_cuisine": food_preferences.general_cuisine,
                    "general_cuisine_notes": food_preferences.general_cuisine_notes,
                    "fish_and_shellfish": food_preferences.fish_and_shellfish,
                    "fish_and_shellfish_notes": food_preferences.fish_and_shellfish_notes,
                    "meat": food_preferences.meat,
                    "meat_notes": food_preferences.meat_notes,
                    "bread": food_preferences.bread,
                    "bread_notes": food_preferences.bread_notes,
                    "soup": food_preferences.soup,
                    "soup_notes": food_preferences.soup_notes,
                    "salad": food_preferences.salad,
                    "salad_notes": food_preferences.salad_notes,
                    "cheese": food_preferences.cheese,
                    "cheese_notes": food_preferences.cheese_notes,
                    "dessert": food_preferences.dessert,
                    "dessert_notes": food_preferences.dessert_notes,
                    "kids_meals": food_preferences.kids_meals,
                    "kids_meals_notes": food_preferences.kids_meals_notes,
                    "kids_allergies": food_preferences.kids_allergies,
                },
                view="onboarding",
            )
    ctx = {"form": form, "onboarding": True}

    return render(request, "guests/onboarding/preferences_food.html", ctx)


@login_required
@guest_required
def onboarding_meals_room(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    guest_details = user.guest_profile.details
    ctx = {"form": MealAndRoomPreferencesForm(view="onboarding")}

    breakfast_selection = None
    lunch_selection = None
    dinner_selection = None
    meal_and_room_preferences = (
        guest_details.meal_and_room_preferences
        if hasattr(guest_details, "meal_and_room_preferences")
        else None
    )
    if meal_and_room_preferences:
        breakfast_selection = meal_and_room_preferences.breakfast_selection
        lunch_selection = meal_and_room_preferences.lunch_selection
        dinner_selection = meal_and_room_preferences.dinner_selection
    if request.method == "POST":
        form = MealAndRoomPreferencesForm(data=request.POST)
        if form.is_valid():
            if not meal_and_room_preferences:
                meal_and_room_preferences = create_meal_and_room_preferences(
                    guest=guest_details,
                    dietary_restrictions=request.POST["dietary_restrictions"],
                    dietary_restrictions_other_notes=form.cleaned_data[
                        "dietary_restrictions_other_notes"
                    ],
                    dietary_restrictions_notes=form.cleaned_data[
                        "dietary_restrictions_notes"
                    ],
                    breakfast_time=form.cleaned_data["breakfast_time"],
                    breakfast_selection=form.cleaned_data["breakfast_selection"],
                    breakfast_note=form.cleaned_data["breakfast_note"],
                    lunch_time=form.cleaned_data["lunch_time"],
                    lunch_selection=form.cleaned_data["lunch_selection"],
                    lunch_note=form.cleaned_data["lunch_note"],
                    dinner_time=form.cleaned_data["dinner_time"],
                    dinner_selection=form.cleaned_data["dinner_selection"],
                    dinner_note=form.cleaned_data["dinner_note"],
                    canapes_time=form.cleaned_data["canapes_time"],
                    canapes_selection=request.POST["canapes_selection"],
                    midmorning_snacks=request.POST["midmorning_snacks"],
                    midafternoon_snacks=request.POST["midafternoon_snacks"],
                )
            else:
                update_meal_and_room_preferences(
                    meal_and_room_preferences=meal_and_room_preferences,
                    canapes_selection=request.POST["canapes_selection"],
                    dietary_restrictions=request.POST["dietary_restrictions"],
                    midmorning_snacks=request.POST["midmorning_snacks"],
                    midafternoon_snacks=request.POST["midafternoon_snacks"],
                    **form.cleaned_data,
                )
            return redirect(reverse("guests:onboarding_diet_services"))
    else:
        if meal_and_room_preferences:
            initial_fields = {
                "dietary_restrictions_other_notes": meal_and_room_preferences.dietary_restrictions_other_notes,
                "dietary_restrictions_notes": meal_and_room_preferences.dietary_restrictions_notes,
                "breakfast_time": meal_and_room_preferences.breakfast_time,
                "breakfast_selection": breakfast_selection.name,
                "breakfast_note": meal_and_room_preferences.breakfast_note,
                "lunch_time": meal_and_room_preferences.lunch_time,
                "lunch_selection": lunch_selection.name,
                "lunch_note": meal_and_room_preferences.lunch_note,
                "dinner_time": meal_and_room_preferences.dinner_time,
                "dinner_selection": dinner_selection.name,
                "dinner_note": meal_and_room_preferences.dinner_note,
                "canapes_time": meal_and_room_preferences.canapes_time,
            }
            ctx["canapes_selection"] = meal_and_room_preferences.canapes_selection
            ctx["midmorning_snacks"] = meal_and_room_preferences.midmorning_snacks
            ctx["midafternoon_snacks"] = meal_and_room_preferences.midafternoon_snacks
            ctx["dietary_restrictions"] = meal_and_room_preferences.dietary_restrictions
            ctx["form"] = MealAndRoomPreferencesForm(
                initial=initial_fields, view="onboarding"
            )

    return render(request, "guests/onboarding/meals_and_room.html", ctx)


@login_required
@guest_required
def onboarding_diet_services(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    guest_details = user.guest_profile.details
    ctx = {}
    other_services = None

    diet_services_sizes_preferences = (
        guest_details.diet_services_sizes_preferences
        if hasattr(guest_details, "diet_services_sizes_preferences")
        else None
    )

    if diet_services_sizes_preferences:
        other_services = (
            diet_services_sizes_preferences.other_service
            if hasattr(diet_services_sizes_preferences, "other_service")
            else None
        )
    if request.method == "POST":
        form = DietServicesSizesForm(data=request.POST, view="onboarding")
        if form.is_valid():
            if not diet_services_sizes_preferences:
                diet_services_sizes_preferences = (
                    create_diet_services_sizes_preferences(
                        guest=guest_details,
                        preferred_room_temperature=form.cleaned_data[
                            "preferred_room_temperature"
                        ],
                        other_services=request.POST.getlist("other_services", ""),
                        other_services_other_notes=form.cleaned_data[
                            "other_services_other_notes"
                        ],
                        shirt_sizing=request.POST["shirt_sizing"],
                        international_shirt_sizing=request.POST[
                            "international_shirt_sizing"
                        ],
                        shirt_size=request.POST["shirt_size"],
                        shoe_sizing=request.POST["shoe_sizing"],
                        international_shoe_sizing=request.POST[
                            "international_shoe_sizing"
                        ],
                        shoe_size=form.cleaned_data["shoe_size"],
                        favorite_flowers=form.cleaned_data["favorite_flowers"],
                    )
                )
            else:
                update_diet_services_sizes_preferences(
                    diet_services_sizes_preferences=diet_services_sizes_preferences,
                    other_services=request.POST.getlist("other_services", ""),
                    shirt_sizing=request.POST["shirt_sizing"],
                    international_shirt_sizing=request.POST[
                        "international_shirt_sizing"
                    ],
                    shirt_size=request.POST["shirt_size"],
                    shoe_sizing=request.POST["shoe_sizing"],
                    international_shoe_sizing=request.POST["international_shoe_sizing"],
                    **form.cleaned_data,
                )
            return redirect(reverse("guests:onboarding_beverages"))
    else:
        form = DietServicesSizesForm()
        if diet_services_sizes_preferences:
            initial_fields = {
                "preferred_room_temperature": diet_services_sizes_preferences.preferred_room_temperature,
                "other_services_other_notes": diet_services_sizes_preferences.other_services_other_notes,
                "shoe_size": diet_services_sizes_preferences.shoe_size,
                "favorite_flowers": diet_services_sizes_preferences.favorite_flowers,
            }
            ctx["other_services"] = other_services.name
            ctx["shirt_sizing"] = diet_services_sizes_preferences.shirt_sizing
            ctx[
                "international_shirt_sizing"
            ] = diet_services_sizes_preferences.international_shirt_sizing
            ctx["shirt_size"] = diet_services_sizes_preferences.shirt_size
            ctx["shoe_sizing"] = diet_services_sizes_preferences.shoe_sizing
            ctx[
                "international_shoe_sizing"
            ] = diet_services_sizes_preferences.international_shoe_sizing
            form = DietServicesSizesForm(initial=initial_fields, view="onboarding")

    ctx["form"] = form
    return render(request, "guests/onboarding/diet_services.html", ctx)


@login_required
@guest_required
def onboarding_beverages(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    guest_details = user.guest_profile.details
    beverages_and_alcoholic_preferences = (
        guest_details.beverages_and_alcoholic_preferences
        if hasattr(guest_details, "beverages_and_alcoholic_preferences")
        else None
    )
    ctx = {"guest": guest_details}
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

    if request.method == "POST":
        form = BeveragesAlcoholPreferencesForm(
            data=request.POST, alcoholic_preferences=beverages_and_alcoholic_preferences
        )
        if form.is_valid():
            if not beverages_and_alcoholic_preferences:
                beverages_and_alcoholic_preferences = (
                    create_beverages_alcohol_preferences(
                        guest=guest_details,
                        milk_selection=form.cleaned_data["milk_selection"],
                        milk_note=form.cleaned_data["milk_note"],
                        coffee_selection=form.cleaned_data["coffee_selection"],
                        coffee_note=form.cleaned_data["coffee_note"],
                        tea_selection=form.cleaned_data["tea_selection"],
                        tea_note=form.cleaned_data["tea_note"],
                        water_selection=form.cleaned_data["water_selection"],
                        water_note=form.cleaned_data["water_note"],
                        juice_selection=form.cleaned_data["juice_selection"],
                        juice_note=form.cleaned_data["juice_note"],
                        sodas_and_mixers_selection=form.cleaned_data[
                            "sodas_and_mixers_selection"
                        ],
                        sodas_and_mixers_note=form.cleaned_data[
                            "sodas_and_mixers_note"
                        ],
                        add_ons_selection=form.cleaned_data["add_ons_selection"],
                        add_ons_note=form.cleaned_data["add_ons_note"],
                        whiskey_name=request.POST["whiskey_name"],
                        whiskey_quantity=request.POST["whiskey_quantity"],
                        extra_whiskey=get_additional_alcohol("whiskey", request.POST),
                        brandy_name=request.POST["brandy_name"],
                        brandy_quantity=request.POST["brandy_quantity"],
                        extra_brandy=get_additional_alcohol("brandy", request.POST),
                        vodka_name=request.POST["vodka_name"],
                        vodka_quantity=request.POST["vodka_quantity"],
                        extra_vodka=get_additional_alcohol("vodka", request.POST),
                        tequila_name=request.POST["tequila_name"],
                        tequila_quantity=request.POST["tequila_quantity"],
                        extra_tequila=get_additional_alcohol("tequila", request.POST),
                        rum_name=request.POST["rum_name"],
                        rum_quantity=request.POST["rum_quantity"],
                        extra_rum=get_additional_alcohol("rum", request.POST),
                        liquors_name=request.POST["liquors_name"],
                        liquors_quantity=request.POST["liquors_quantity"],
                        extra_liquors=get_additional_alcohol("liquors", request.POST),
                        cocktail_name=request.POST["cocktail_name"],
                        cocktail_quantity=request.POST["cocktail_quantity"],
                        extra_cocktail=get_additional_alcohol("cocktail", request.POST),
                        port_beer_name=request.POST["port_beer_name"],
                        port_beer_quantity=request.POST["port_beer_quantity"],
                        extra_port_beer=get_additional_alcohol(
                            "port_beer", request.POST
                        ),
                        red_wine_name=request.POST["red_wine_name"],
                        red_wine_quantity=request.POST["red_wine_quantity"],
                        extra_red_wine=get_additional_alcohol("red_wine", request.POST),
                        white_wine_name=request.POST["white_wine_name"],
                        white_wine_quantity=request.POST["white_wine_quantity"],
                        extra_white_wine=get_additional_alcohol(
                            "white_wine", request.POST
                        ),
                        rose_wine_name=request.POST["rose_wine_name"],
                        rose_wine_quantity=request.POST["rose_wine_quantity"],
                        extra_rose_wine=get_additional_alcohol(
                            "rose_wine", request.POST
                        ),
                        champagne_name=request.POST["champagne_name"],
                        champagne_quantity=request.POST["champagne_quantity"],
                        extra_champagne=get_additional_alcohol(
                            "champagne", request.POST
                        ),
                        other_name=request.POST["other_name"],
                        other_quantity=request.POST["other_quantity"],
                    )
                )
            else:
                update_beverages_alcohol_preferences(
                    beverages_and_alcoholic_preferences=beverages_and_alcoholic_preferences,
                    whiskey_name=request.POST["whiskey_name"],
                    whiskey_quantity=request.POST["whiskey_quantity"],
                    extra_whiskey=get_additional_alcohol("whiskey", request.POST),
                    brandy_name=request.POST["brandy_name"],
                    brandy_quantity=request.POST["brandy_quantity"],
                    extra_brandy=get_additional_alcohol("brandy", request.POST),
                    vodka_name=request.POST["vodka_name"],
                    vodka_quantity=request.POST["vodka_quantity"],
                    extra_vodka=get_additional_alcohol("vodka", request.POST),
                    tequila_name=request.POST["tequila_name"],
                    tequila_quantity=request.POST["tequila_quantity"],
                    extra_tequila=get_additional_alcohol("tequila", request.POST),
                    rum_name=request.POST["rum_name"],
                    rum_quantity=request.POST["rum_quantity"],
                    extra_rum=get_additional_alcohol("rum", request.POST),
                    liquors_name=request.POST["liquors_name"],
                    liquors_quantity=request.POST["liquors_quantity"],
                    extra_liquors=get_additional_alcohol("liquors", request.POST),
                    cocktail_name=request.POST["cocktail_name"],
                    cocktail_quantity=request.POST["cocktail_quantity"],
                    extra_cocktail=get_additional_alcohol("cocktail", request.POST),
                    port_beer_name=request.POST["port_beer_name"],
                    port_beer_quantity=request.POST["port_beer_quantity"],
                    extra_port_beer=get_additional_alcohol("port_beer", request.POST),
                    red_wine_name=request.POST["red_wine_name"],
                    red_wine_quantity=request.POST["red_wine_quantity"],
                    extra_red_wine=get_additional_alcohol("red_wine", request.POST),
                    white_wine_name=request.POST["white_wine_name"],
                    white_wine_quantity=request.POST["white_wine_quantity"],
                    extra_white_wine=get_additional_alcohol("white_wine", request.POST),
                    rose_wine_name=request.POST["rose_wine_name"],
                    rose_wine_quantity=request.POST["rose_wine_quantity"],
                    extra_rose_wine=get_additional_alcohol("rose_wine", request.POST),
                    champagne_name=request.POST["champagne_name"],
                    champagne_quantity=request.POST["champagne_quantity"],
                    extra_champagne=get_additional_alcohol("champagne", request.POST),
                    other_name=request.POST["other_name"],
                    other_quantity=request.POST["other_quantity"],
                    **form.cleaned_data,
                )
            return redirect(reverse("guests:dashboard"))
    else:
        form = BeveragesAlcoholPreferencesForm(
            view="onboarding", alcoholic_preferences=beverages_and_alcoholic_preferences
        )
        if beverages_and_alcoholic_preferences:
            initial_fields = {
                "milk_note": beverages_and_alcoholic_preferences.milk_note,
                "coffee_note": beverages_and_alcoholic_preferences.coffee_note,
                "tea_note": beverages_and_alcoholic_preferences.tea_note,
                "water_note": beverages_and_alcoholic_preferences.water_note,
                "juice_note": beverages_and_alcoholic_preferences.juice_note,
                "sodas_and_mixers_note": beverages_and_alcoholic_preferences.sodas_and_mixers_note,
                "add_ons_note": beverages_and_alcoholic_preferences.add_ons_note,
                "milk_selection": milk_selection.name,
                "coffee_selection": coffee_selection.name,
                "tea_selection": tea_selection.name,
                "water_selection": water_selection.name,
                "juice_selection": juice_selection.name,
                "sodas_and_mixers_selection": sodas_and_mixers_selection.name,
                "add_ons_selection": add_ons_selection.name,
            }
            form = BeveragesAlcoholPreferencesForm(
                initial=initial_fields,
                view="onboarding",
                alcoholic_preferences=beverages_and_alcoholic_preferences,
            )

    ctx["form"] = form

    return render(request, "guests/onboarding/beverage_and_alcoholic.html", ctx)


@login_required
@guest_required
def trips(request: HttpRequest) -> HttpResponse:
    user: User = request.user

    current_date = timezone.now().date()
    guest: GuestDetail = user.guest_details
    complete_preferences = (
        guest.has_diet_services_sizes_pref and guest.has_beverages_and_alcoholic_pref
    )

    trips = guest.charters.filter(
        embark_date__gte=current_date, is_complete=True
    ).order_by("-embark_date")
    ctx = {
        "guest": guest,
        "trips": trips,
        "user": user,
        "title": "Trips",
        "active": "trips",
        "completed_preferences": complete_preferences,
    }
    return render(request, "guests/trips.html", ctx)


@login_required
@guest_required
def trip_details(request: HttpRequest, charter_id: int) -> HttpResponse:
    user: User = request.user
    guest: GuestDetail = user.guest_details
    try:
        charter: Charter = Charter.objects.get(id=charter_id)
    except Charter.DoesNotExist as err:
        print(err)
        messages.error(request, "Trip does not exist")
        return redirect(reverse("guests:trips"))

    if guest not in charter.guests.all() or guest != charter.principal_guest:
        messages.error(request, "Invalid action. You are not included in this trip.")
        return redirect(reverse("guests:trips"))

    ctx = {
        "trip": charter,
        "user": user,
        "guest": guest,
        "active": "trips",
    }
    return render(request, "guests/trip_details.html", ctx)


@login_required
@guest_required
def profile_settings(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    guest = user.guest_details
    title = "Your Profile"
    data = {}
    image_form = ProfileImageForm(user=user)
    document_form = DocumentForm()
    if request.method == "POST":
        form = PrincipleOnboardingForm(
            request.POST,
            request.FILES,
            view="profile_settings",
            user=user,
        )

        if form.is_valid():
            data = {
                "first_name": form.cleaned_data.get("first_name"),
                "last_name": form.cleaned_data.get("last_name"),
                "email": form.cleaned_data.get("email"),
                "phone_number": form.cleaned_data.get("phone_number"),
                "emergency_contact": form.cleaned_data.get("emergency_contact"),
                "emergency_relation": form.cleaned_data.get("emergency_relation"),
                "emergency_phone": form.cleaned_data.get("emergency_phone"),
                "address_street": form.cleaned_data.get("address_street"),
                "address_number": form.cleaned_data.get("address_number"),
                "address_city": form.cleaned_data.get("address_city"),
                "address_state": form.cleaned_data.get("address_state"),
                "address_zipcode": form.cleaned_data.get("address_zipcode"),
                "address_country": form.cleaned_data.get("address_country"),
                "nationality": form.cleaned_data.get("nationality"),
                "passport": form.cleaned_data.get("passport"),
                "passport_number": form.cleaned_data.get("passport_number"),
                "passport_expiration": form.cleaned_data.get("passport_expiration"),
                "date_of_birth": form.cleaned_data.get("date_of_birth"),
                "medical_issues": form.cleaned_data.get("medical_issues"),
                "allergies": form.cleaned_data.get("allergies"),
                "medications": form.cleaned_data.get("medications"),
                "salutation_nickname": form.cleaned_data.get("salutation_nickname"),
                "high_priority_details": form.cleaned_data.get("high_priority_details"),
                "lactose_intolerant": form.cleaned_data.get("lactose_intolerant"),
                "shellfish_allergy": form.cleaned_data.get("shellfish_allergy"),
                "nut_allergy": form.cleaned_data.get("nut_allergy"),
                "gluten_free": form.cleaned_data.get("gluten_free"),
                "none_food_sensitivity": form.cleaned_data.get("none_food_sensitivity"),
                "other": form.cleaned_data.get("other"),
                "other_notes": form.cleaned_data.get("other_notes"),
            }

            if not hasattr(user.guest_profile, "details"):
                create_guest_detail(
                    user=user,
                    **data,
                )
            else:
                update_guest_detail(
                    guest_detail=user.guest_profile.details,
                    **data,
                )
            messages.success(request, "Successfully updated your profile.")
            return redirect(reverse("guests:profile"))
    else:
        initial = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        if hasattr(user, "guest_profile"):
            initial["phone_number"] = user.guest_profile.phone_number
            if hasattr(user.guest_profile, "details"):
                details = user.guest_profile.details
                data = {
                    "emergency_contact": details.emergency_contact,
                    "emergency_relation": details.emergency_relation,
                    "emergency_phone": details.emergency_phone,
                    "address_street": details.address_street,
                    "address_number": details.address_number,
                    "address_city": details.address_city,
                    "address_state": details.address_state,
                    "address_zipcode": details.address_zipcode,
                    "address_country": details.address_country,
                    "nationality": details.nationality,
                    "passport_number": details.passport_number,
                    "passport_expiration": details.passport_expiration.strftime(
                        "%m/%d/%Y"
                    )
                    if details.passport_expiration
                    else None,
                    "passport": details.passport,
                    "date_of_birth": details.date_of_birth.strftime("%m/%d/%Y")
                    if details.date_of_birth
                    else None,
                    "medical_issues": details.medical_issues,
                    "allergies": details.allergies,
                    "medications": details.medications,
                    "salutation_nickname": details.salutation_nickname,
                    "high_priority_details": details.high_priority_details,
                    "lactose_intolerant": details.lactose_intolerant,
                    "shellfish_allergy": details.shellfish_allergy,
                    "nut_allergy": details.nut_allergy,
                    "gluten_free": details.gluten_free,
                    "none_food_sensitivity": details.none_food_sensitivity,
                    "other": details.other,
                    "other_notes": details.other_notes,
                }
        initial = {**initial, **data}
        form = PrincipleOnboardingForm(
            initial=initial, view="profile_settings", user=user
        )

    ctx = {
        "user": user,
        "form": form,
        "active": "profile",
        "image_form": image_form,
        "guest": guest,
        "title": title,
        "document_form": document_form,
        "documents": Document.objects.filter(
            model=Document.ModelChoices.GUEST_DETAIL,
            model_id=guest.id,
        ),
    }
    return render(request, "guests/profile.html", ctx)


def profile_image_upload(request: HttpRequest) -> JsonResponse:

    user: User = request.user
    image_form = ProfileImageForm(request.POST, request.FILES, user=user)
    if image_form.is_valid():
        user.profile_picture.delete()
        user.profile_picture = image_form.cleaned_data.get("profile_picture")
        user.save()
        return JsonResponse({"url": user.profile_picture.url})
    return JsonResponse({"error": "Please upload a valid image."})


def upload_documents(request: HttpRequest) -> JsonResponse:

    user: User = request.user
    document_form = DocumentForm(request.POST, request.FILES)
    if document_form.is_valid():
        document_list = []
        for f in request.FILES.getlist("document"):
            document_list.append(
                Document(
                    model_id=user.guest_details.id,
                    model=Document.ModelChoices.GUEST_DETAIL,
                    uploaded_by=user,
                    document=f,
                )
            )
    if document_list:
        Document.objects.bulk_create(document_list)
    return redirect("guests:profile")


def download_passport(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    guest: GuestDetail = user.guest_details
    filename: str = guest.passport.name.split("/")[-1]
    response = HttpResponse(guest.passport, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response


def privacy_policy(request: HttpRequest) -> HttpResponse:
    ctx = {"user": request.user, "title": "Privacy Policy"}
    return render(request, "guests/privacy_policy.html", ctx)


def terms_and_conditions(request: HttpRequest) -> HttpResponse:
    ctx = {"user": request.user, "title": "Terms and Conditions"}
    return render(request, "guests/terms_and_conditions.html", ctx)
