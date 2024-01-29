from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from authentication.decorators import guest_required
from admins.tasks import has_completed_preferences
from charter.helpers import (
    generate_guest_details_pdf,
    generate_short_jet_pdf,
    generate_long_jet_pdf,
)
from charter.models import GuestDetail
from preferences.forms import (
    BeveragesAlcoholPreferencesForm,
    DietServicesSizesForm,
    FoodPreferencesForm,
    LongJetPreferencesForm,
    MealAndRoomPreferencesForm,
    ShortJetPreferencesForm,
)
from preferences.helpers import get_max_pref_created_date, get_additional_alcohol

from admins.models import User
from preferences.models import LongJetPreferenceSheet, ShortJetPreferenceSheet
from preferences.services import (
    create_beverages_alcohol_preferences,
    create_long_jet_preferences,
    create_diet_services_sizes_preferences,
    create_food_preferences,
    create_meal_and_room_preferences,
    create_short_jet_preferences,
    update_beverages_alcohol_preferences,
    update_diet_services_sizes_preferences,
    update_food_preferences,
    update_long_jet_preferences,
    update_meal_and_room_preferences,
    update_short_jet_preferences,
)


@login_required
@guest_required
def food_preferences(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    guest_details = user.guest_profile.details
    food_preferences = (
        guest_details.food_preferences
        if hasattr(guest_details, "food_preferences")
        else None
    )

    ctx = {
        "title": "Preferences",
        "guest": guest_details,
        "pref_created_date": get_max_pref_created_date(guest_details),
    }

    if request.method == "POST":
        form = FoodPreferencesForm(data=request.POST)
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
                    kids_meals=form.cleaned_data["kids_meals"],
                    kids_meals_notes=form.cleaned_data["kids_meals_notes"],
                    kids_allergies=form.cleaned_data["kids_allergies"],
                )
            else:
                update_food_preferences(
                    food_preferences=food_preferences, **form.cleaned_data
                )
            has_completed_preferences.delay(guest_details.id)
            messages.success(request, "Successfully updated your preferences.")
            return redirect(
                reverse(
                    "preferences:meal_and_room_preferences",
                )
            )
    else:
        form = FoodPreferencesForm()
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
                }
            )

    ctx["food_preferences_form"] = form
    has_completed_preferences.delay(guest_details.id)

    return render(request, "preferences/principal_food_preferences.html", ctx)


@login_required
@guest_required
def meal_and_room_preferences(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    guest_details = user.guest_profile.details

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

    ctx = {
        "title": "Preferences",
        "guest": guest_details,
        "breakfast_selection": breakfast_selection,
        "lunch_selection": lunch_selection,
        "dinner_selection": dinner_selection,
        "pref_created_date": get_max_pref_created_date(guest_details),
    }

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
                    midmorning_snacks=request.POST["midmorning_snacks"],
                    midafternoon_snacks=request.POST["midafternoon_snacks"],
                    dietary_restrictions=request.POST["dietary_restrictions"],
                    **form.cleaned_data,
                )
            has_completed_preferences.delay(guest_details.id)
            messages.success(request, "Successfully updated your preferences.")
            return redirect(reverse("preferences:diet_services_sizing"))
    else:
        form = MealAndRoomPreferencesForm()
        if meal_and_room_preferences:
            initial_fields = {
                "breakfast_time": meal_and_room_preferences.breakfast_time,
                "breakfast_selection": breakfast_selection.name,
                "dietary_restrictions_other_notes": meal_and_room_preferences.dietary_restrictions_other_notes,
                "dietary_restrictions_notes": meal_and_room_preferences.dietary_restrictions_notes,
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
            ctx["dietary_restrictions"] = meal_and_room_preferences.dietary_restrictions
            ctx["midafternoon_snacks"] = meal_and_room_preferences.midafternoon_snacks
            form = MealAndRoomPreferencesForm(initial=initial_fields)

    ctx["meal_and_room_preferences_form"] = form
    has_completed_preferences.delay(guest_details.id)
    return render(request, "preferences/principal_meal_and_room_preferences.html", ctx)


@login_required
@guest_required
def diet_services_sizing(
    request: HttpRequest,
) -> HttpResponse:
    user: User = request.user
    guest_details = user.guest_profile.details
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

    ctx = {
        "title": "Preferences",
        "guest": guest_details,
        "pref_created_date": get_max_pref_created_date(guest_details),
    }

    if request.method == "POST":
        form = DietServicesSizesForm(data=request.POST)
        if form.is_valid():
            if not diet_services_sizes_preferences:
                diet_services_sizes_preferences = (
                    create_diet_services_sizes_preferences(
                        guest=guest_details,
                        favorite_flowers=form.cleaned_data["favorite_flowers"],
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
            has_completed_preferences.delay(guest_details.id)
            messages.success(request, "Successfully updated your preferences.")
            return redirect(reverse("preferences:beverage_alcohol"))
    else:
        form = DietServicesSizesForm()
        if diet_services_sizes_preferences:
            initial_fields = {
                "preferred_room_temperature": diet_services_sizes_preferences.preferred_room_temperature,
                "other_services_other_notes": diet_services_sizes_preferences.other_services_other_notes,
                "favorite_flowers": diet_services_sizes_preferences.favorite_flowers,
                "shoe_size": diet_services_sizes_preferences.shoe_size,
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
            form = DietServicesSizesForm(initial=initial_fields)

    ctx["diet_services_sizing_form"] = form
    has_completed_preferences.delay(guest_details.id)
    return render(request, "preferences/all_guests_diet_services_sizing.html", ctx)


@login_required
@guest_required
def beverage_alcohol(
    request: HttpRequest,
) -> HttpResponse:
    user: User = request.user
    guest_details = user.guest_profile.details
    beverages_and_alcoholic_preferences = (
        guest_details.beverages_and_alcoholic_preferences
        if hasattr(guest_details, "beverages_and_alcoholic_preferences")
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
        "title": "Preferences",
        "guest": guest_details,
        "pref_created_date": get_max_pref_created_date(guest_details),
    }

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
            has_completed_preferences.delay(guest_details.id)
            messages.success(request, "Successfully updated your preferences.")
            return redirect(reverse("preferences:beverage_alcohol"))
    else:
        form = BeveragesAlcoholPreferencesForm(
            alcoholic_preferences=beverages_and_alcoholic_preferences
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
                alcoholic_preferences=beverages_and_alcoholic_preferences,
            )

    ctx["beverages_alcohol_form"] = form
    return render(request, "preferences/all_guests_beverage_alcohol.html", ctx)


@login_required
@guest_required
def download_preferences_pdf(
    request: HttpRequest,
) -> HttpResponse:
    user: User = request.user
    guest_details = user.guest_profile.details
    charter = None

    response = generate_guest_details_pdf(request, guest_details, charter)
    return response


@login_required
@guest_required
def short_jet_preference(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    guest_details: GuestDetail = user.guest_profile.details
    short_jet_preference: ShortJetPreferenceSheet = (
        guest_details.short_jet_preference
        if hasattr(guest_details, "short_jet_preference")
        else None
    )

    form = ShortJetPreferencesForm()

    ctx = {
        "guest": guest_details,
        "user": user,
        "title": "Short Jet Preferences | Harpoon",
    }
    if request.method == "POST":
        form = ShortJetPreferencesForm(data=request.POST)
        if form.is_valid():
            if not short_jet_preference:
                create_short_jet_preferences(
                    guest=guest_details,
                    dietary_restrictions=request.POST.get("dietary_restrictions"),
                    dietary_restrictions_notes=form.cleaned_data.get(
                        "dietary_restrictions_notes"
                    ),
                    dietary_restrictions_other_notes=form.cleaned_data.get(
                        "dietary_restrictions_other_notes"
                    ),
                    breakfast=form.cleaned_data.get("breakfast"),
                    breakfast_notes=form.cleaned_data.get("breakfast_notes"),
                    lunch=form.cleaned_data.get("lunch"),
                    lunch_notes=form.cleaned_data.get("lunch_notes"),
                    dinner=form.cleaned_data.get("dinner"),
                    dinner_notes=form.cleaned_data.get("dinner_notes"),
                    kids_meals=form.cleaned_data.get("kids_meals"),
                    kids_allergies=form.cleaned_data.get("kids_allergies"),
                    kids_meals_notes=form.cleaned_data.get("kids_meals_notes"),
                    favorite_flowers=form.cleaned_data.get("favorite_flowers"),
                )
                messages.success(
                    request, "Successfully Created Short Leg Jet Preferences Sheet"
                )
                return redirect(reverse("guests:trips"))
            else:
                short_jet_preference = update_short_jet_preferences(
                    instance=short_jet_preference,
                    dietary_restrictions=request.POST.get("dietary_restrictions"),
                    dietary_restrictions_notes=form.cleaned_data.get(
                        "dietary_restrictions_notes"
                    ),
                    dietary_restrictions_other_notes=form.cleaned_data.get(
                        "dietary_restrictions_other_notes"
                    ),
                    breakfast=form.cleaned_data.get("breakfast"),
                    breakfast_notes=form.cleaned_data.get("breakfast_notes"),
                    lunch=form.cleaned_data.get("lunch"),
                    lunch_notes=form.cleaned_data.get("lunch_notes"),
                    dinner=form.cleaned_data.get("dinner"),
                    dinner_notes=form.cleaned_data.get("dinner_notes"),
                    kids_meals=form.cleaned_data.get("kids_meals"),
                    kids_allergies=form.cleaned_data.get("kids_allergies"),
                    kids_meals_notes=form.cleaned_data.get("kids_meals_notes"),
                    favorite_flowers=form.cleaned_data.get("favorite_flowers"),
                )
                messages.success(
                    request, "Successfully Updated Short Leg Jet Preferences Sheet"
                )
                return redirect(reverse("guests:trips"))

    if short_jet_preference:
        ctx["dietary_restrictions"] = short_jet_preference.dietary_restrictions
        initial_fields = {
            "dietary_restrictions": short_jet_preference.dietary_restrictions,
            "dietary_restrictions_notes": short_jet_preference.dietary_restrictions_notes,
            "dietary_restrictions_other_notes": short_jet_preference.dietary_restrictions_other_notes,
            "breakfast": short_jet_preference.breakfast,
            "breakfast_notes": short_jet_preference.breakfast_notes,
            "lunch": short_jet_preference.lunch,
            "lunch_notes": short_jet_preference.lunch_notes,
            "dinner": short_jet_preference.dinner,
            "dinner_notes": short_jet_preference.dinner_notes,
            "kids_meals": short_jet_preference.kids_meals,
            "kids_allergies": short_jet_preference.kids_allergies,
            "kids_meals_notes": short_jet_preference.kids_meals_notes,
            "favorite_flowers": short_jet_preference.favorite_flowers,
        }
        form = ShortJetPreferencesForm(initial=initial_fields)

    ctx["form"] = form
    return render(request, "preferences/short_jet.html", ctx)


@login_required
@guest_required
def long_jet_preference(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    guest_details = user.guest_profile.details

    long_jet_preference: LongJetPreferenceSheet = (
        guest_details.long_jet_preference
        if hasattr(guest_details, "long_jet_preference")
        else None
    )

    form = LongJetPreferencesForm()

    ctx = {
        "guest": guest_details,
        "user": user,
        "title": "Long Jet Preferences | Harpoon",
    }

    if request.method == "POST":
        form = LongJetPreferencesForm(data=request.POST)
        if form.is_valid():
            if not long_jet_preference:
                create_long_jet_preferences(
                    guest=guest_details,
                    dietary_restrictions=request.POST.get("dietary_restrictions"),
                    dietary_restrictions_notes=form.cleaned_data.get(
                        "dietary_restrictions_notes"
                    ),
                    dietary_restrictions_other_notes=form.cleaned_data.get(
                        "dietary_restrictions_other_notes"
                    ),
                    breakfast=form.cleaned_data.get("breakfast"),
                    breakfast_notes=form.cleaned_data.get("breakfast_notes"),
                    lunch=form.cleaned_data.get("lunch"),
                    lunch_notes=form.cleaned_data.get("lunch_notes"),
                    dinner=form.cleaned_data.get("dinner"),
                    dinner_notes=form.cleaned_data.get("dinner_notes"),
                    fresh_snacks=form.cleaned_data.get("fresh_snacks"),
                    fresh_snacks_notes=form.cleaned_data.get("fresh_snacks_notes"),
                    pantry_snacks=form.cleaned_data.get("pantry_snacks"),
                    pantry_snacks_notes=form.cleaned_data.get("pantry_snacks_notes"),
                    kids_meals=form.cleaned_data.get("kids_meals"),
                    kids_allergies=form.cleaned_data.get("kids_allergies"),
                    kids_meals_notes=form.cleaned_data.get("kids_meals_notes"),
                    favorite_flowers=form.cleaned_data.get("favorite_flowers"),
                )
                messages.success(
                    request, "Successfully Created Long Leg Jet Preferences Sheet"
                )
                return redirect(reverse("guests:trips"))
            else:
                long_jet_preference = update_long_jet_preferences(
                    instance=long_jet_preference,
                    dietary_restrictions=request.POST.get("dietary_restrictions"),
                    dietary_restrictions_notes=form.cleaned_data.get(
                        "dietary_restrictions_notes"
                    ),
                    dietary_restrictions_other_notes=form.cleaned_data.get(
                        "dietary_restrictions_other_notes"
                    ),
                    breakfast=form.cleaned_data.get("breakfast"),
                    breakfast_notes=form.cleaned_data.get("breakfast_notes"),
                    lunch=form.cleaned_data.get("lunch"),
                    lunch_notes=form.cleaned_data.get("lunch_notes"),
                    dinner=form.cleaned_data.get("dinner"),
                    dinner_notes=form.cleaned_data.get("dinner_notes"),
                    fresh_snacks=form.cleaned_data.get("fresh_snacks"),
                    fresh_snacks_notes=form.cleaned_data.get("fresh_snacks_notes"),
                    pantry_snacks=form.cleaned_data.get("pantry_snacks"),
                    pantry_snacks_notes=form.cleaned_data.get("pantry_snacks_notes"),
                    kids_meals=form.cleaned_data.get("kids_meals"),
                    kids_allergies=form.cleaned_data.get("kids_allergies"),
                    kids_meals_notes=form.cleaned_data.get("kids_meals_notes"),
                    favorite_flowers=form.cleaned_data.get("favorite_flowers"),
                )
                messages.success(
                    request, "Successfully Updated Long Leg Jet Preferences Sheet"
                )
                return redirect(reverse("guests:trips"))
    if long_jet_preference:
        ctx["dietary_restrictions"] = long_jet_preference.dietary_restrictions
        initial_fields = {
            "dietary_restrictions": long_jet_preference.dietary_restrictions,
            "dietary_restrictions_notes": long_jet_preference.dietary_restrictions_notes,
            "dietary_restrictions_other_notes": long_jet_preference.dietary_restrictions_other_notes,
            "breakfast": long_jet_preference.breakfast,
            "breakfast_notes": long_jet_preference.breakfast_notes,
            "lunch": long_jet_preference.lunch,
            "lunch_notes": long_jet_preference.lunch_notes,
            "dinner": long_jet_preference.dinner,
            "dinner_notes": long_jet_preference.dinner_notes,
            "fresh_snacks": long_jet_preference.fresh_snacks,
            "fresh_snacks_notes": long_jet_preference.fresh_snacks_notes,
            "pantry_snacks": long_jet_preference.pantry_snacks,
            "pantry_snacks_notes": long_jet_preference.pantry_snacks_notes,
            "kids_meals": long_jet_preference.kids_meals,
            "kids_allergies": long_jet_preference.kids_allergies,
            "kids_meals_notes": long_jet_preference.kids_meals_notes,
            "favorite_flowers": long_jet_preference.favorite_flowers,
        }
        form = LongJetPreferencesForm(initial=initial_fields)

    ctx["form"] = form
    return render(request, "preferences/long_jet.html", ctx)


@login_required
@guest_required
def yacht_food_preference(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    guest_details = user.guest_profile.details
    form = FoodPreferencesForm(view="preference")
    food_preferences = (
        guest_details.food_preferences
        if hasattr(guest_details, "food_preferences")
        else None
    )
    if request.method == "POST":
        form = FoodPreferencesForm(data=request.POST, view="preference")
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
                    kids_meals=form.cleaned_data["kids_meals"],
                    kids_meals_notes=form.cleaned_data["kids_meals_notes"],
                    kids_allergies=form.cleaned_data["kids_allergies"],
                )
            else:
                update_food_preferences(
                    food_preferences=food_preferences, **form.cleaned_data
                )
                messages.success(
                    request, "Successfully updated Yacht Food Preferences."
                )
            return redirect(
                reverse(
                    "guests:trips",
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
                view="preference",
            )
    ctx = {"form": form}

    return render(request, "guests/onboarding/preferences_food.html", ctx)


@login_required
@guest_required
def download_short_jet_preferences(
    request: HttpRequest,
) -> HttpResponse:
    user: User = request.user
    guest_details = user.guest_profile.details

    response = generate_short_jet_pdf(request, guest_details)
    return response


@login_required
@guest_required
def download_long_jet_preferences(
    request: HttpRequest,
) -> HttpResponse:
    user: User = request.user
    guest_details = user.guest_profile.details

    response = generate_long_jet_pdf(request, guest_details)
    return response


def add_new_alcohol(request: HttpRequest, alcohol_type: str) -> HttpResponse:
    from random import randint

    label = {
        "whiskey": "Whiskey",
        "brandy": "Brandy",
        "vodka": "Vodka",
        "tequila": "Tequila",
        "rum": "Rum",
        "liquors": "Liquors",
        "cocktail": "Cocktail",
        "port_beer": "Port Beer",
        "red_wine": "Red Wine",
        "white_wine": "White Wine",
        "rose_wine": "Rose Wine",
        "champagne": "Champagne",
    }
    ctx = {
        "alcohol_type": alcohol_type,
        "label": label[alcohol_type],
        "random_int": randint(1, 1000),
    }
    return render(request, "preferences/partials/additional_alcohol.html", ctx)
