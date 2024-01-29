import csv
import tempfile

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from weasyprint import CSS, HTML

from admins.models import CrewProfile
from charter.models import Charter, GuestDetail
from config.settings import GUEST_REGISTER_URL
from preferences.constants import (
    ADD_ONS_SELECTIONS,
    BREAD,
    BREAKFAST,
    CHEESE,
    COFFEE_SELECTIONS,
    DESSERT,
    DINNER,
    FISH_SHELLFISH,
    GENERAL_CUISINE,
    JUICE_SELECTIONS,
    LUNCH,
    MEAT,
    MILK_SELECTIONS,
    OTHER_SERVICES,
    SALAD,
    SODAS_MIXERS_SELECTIONS,
    SOUP,
    TEA_SELECTIONS,
)
from preferences.export_helpers import (
    alcohol_preferences_shopping_list,
    beverage_preferences_shopping_list,
    food_preferences_shopping_list,
)


def auto_increment_booking_id():
    initial_value = 000
    last_booking_id = Charter.objects.all().order_by("id").last()

    if not last_booking_id:
        return str(initial_value).zfill(3)

    last_booking_id_number = last_booking_id.id
    new_booking_id_number = last_booking_id_number + 1
    return str(new_booking_id_number).zfill(3)


FOOD_PREFERENCES = [
    "General Cuisine",
    "Fish and Shellfish",
    "Meat",
    "Bread",
    "Salad",
    "Soup",
    "Cheese",
    "Dessert",
]


def get_food_preferences(writer, guest):
    for category in FOOD_PREFERENCES:
        if category == "General Cuisine":
            type = guest.food_preferences.general_cuisine
            note = guest.food_preferences.general_cuisine_notes
            text_choice = GENERAL_CUISINE
        elif category == "Fish and Shellfish":
            type = guest.food_preferences.fish_and_shellfish
            note = guest.food_preferences.fish_and_shellfish_notes
            text_choice = FISH_SHELLFISH
        elif category == "Meat":
            type = guest.food_preferences.meat
            note = guest.food_preferences.meat_notes
            text_choice = MEAT
        elif category == "Bread":
            type = guest.food_preferences.bread
            note = guest.food_preferences.bread_notes
            text_choice = BREAD
        elif category == "Salad":
            type = guest.food_preferences.salad
            note = guest.food_preferences.salad_notes
            text_choice = SALAD
        elif category == "Soup":
            type = guest.food_preferences.soup
            note = guest.food_preferences.soup_notes
            text_choice = SOUP
        elif category == "Cheese":
            type = guest.food_preferences.cheese
            note = guest.food_preferences.cheese_notes
            text_choice = CHEESE
        elif category == "Dessert":
            type = guest.food_preferences.dessert
            note = guest.food_preferences.dessert_notes
            text_choice = DESSERT

        if "[" and "]" in type:
            for item in eval(type):
                writer.writerow(
                    [
                        guest,
                        "Galley",
                        "Food",
                        category,
                        dict(text_choice)[item],
                        "",
                        note,
                    ]
                )


BEVERAGES_PREFERENCES = [
    "Milk",
    "Coffee",
    "Tea",
    "Water",
    "Juice",
    "Sodas and Mixers",
    "Add Ons",
]


def get_beverages_preferences(writer, guest):
    for category in BEVERAGES_PREFERENCES:
        if category == "Milk":
            type = guest.beverages_and_alcoholic_preferences.milk_selection.name
            note = guest.beverages_and_alcoholic_preferences.milk_note
            text_choice = MILK_SELECTIONS
        elif category == "Coffee":
            type = guest.beverages_and_alcoholic_preferences.coffee_selection.name
            note = guest.beverages_and_alcoholic_preferences.coffee_note
            text_choice = COFFEE_SELECTIONS
        elif category == "Tea":
            type = guest.beverages_and_alcoholic_preferences.tea_selection.name
            note = guest.beverages_and_alcoholic_preferences.tea_note
            text_choice = TEA_SELECTIONS
        elif category == "Juice":
            type = guest.beverages_and_alcoholic_preferences.juice_selection.name
            note = guest.beverages_and_alcoholic_preferences.juice_note
            text_choice = JUICE_SELECTIONS
        elif category == "Sodas and Mixers":
            type = (
                guest.beverages_and_alcoholic_preferences.sodas_and_mixers_selection.name
            )
            note = guest.beverages_and_alcoholic_preferences.sodas_and_mixers_note
            text_choice = SODAS_MIXERS_SELECTIONS
        elif category == "Add Ons":
            type = guest.beverages_and_alcoholic_preferences.add_ons_selection.name
            note = guest.beverages_and_alcoholic_preferences.add_ons_note
            text_choice = ADD_ONS_SELECTIONS
        if "[" and "]" in type:
            for item in eval(type):
                writer.writerow(
                    [
                        guest,
                        "Interior",
                        "Beverages",
                        category,
                        dict(text_choice)[item],
                        "",
                        note,
                    ]
                )


ALCOHOLIC_PREFERENCES = [
    "Whiskey",
    "Brandy",
    "Vodka",
    "Tequila",
    "Rum",
    "Liquours",
    "Cocktail",
    "Port/Beer",
    "Wine (Red)",
    "Wine (White)",
    "Champagne",
]


def get_alcoholic_preferences(writer, guest):
    for alcohol_type in ALCOHOLIC_PREFERENCES:
        if alcohol_type == "Whiskey":
            description = guest.beverages_and_alcoholic_preferences.whiskey_name
            quantity = guest.beverages_and_alcoholic_preferences.whiskey_quantity
        if alcohol_type == "Brandy":
            description = guest.beverages_and_alcoholic_preferences.brandy_name
            quantity = guest.beverages_and_alcoholic_preferences.brandy_quantity
        if alcohol_type == "Vodka":
            description = guest.beverages_and_alcoholic_preferences.vodka_name
            quantity = guest.beverages_and_alcoholic_preferences.vodka_quantity
        if alcohol_type == "Tequila":
            description = guest.beverages_and_alcoholic_preferences.tequila_name
            quantity = guest.beverages_and_alcoholic_preferences.tequila_quantity
        if alcohol_type == "Rum":
            description = guest.beverages_and_alcoholic_preferences.rum_name
            quantity = guest.beverages_and_alcoholic_preferences.rum_quantity
        if alcohol_type == "Liquours":
            description = guest.beverages_and_alcoholic_preferences.liquors_name
            quantity = guest.beverages_and_alcoholic_preferences.liquors_quantity
        if alcohol_type == "Cocktail":
            description = guest.beverages_and_alcoholic_preferences.cocktail_name
            quantity = guest.beverages_and_alcoholic_preferences.cocktail_quantity
        if alcohol_type == "Port/Beer":
            description = guest.beverages_and_alcoholic_preferences.port_beer_name
            quantity = guest.beverages_and_alcoholic_preferences.port_beer_quantity
        if alcohol_type == "Wine (Red)":
            description = guest.beverages_and_alcoholic_preferences.red_wine_name
            quantity = guest.beverages_and_alcoholic_preferences.red_wine_quantity
        if alcohol_type == "Wine (White)":
            description = guest.beverages_and_alcoholic_preferences.white_wine_name
            quantity = guest.beverages_and_alcoholic_preferences.white_wine_quantity
        if alcohol_type == "Wine (Rosé)":
            description = guest.beverages_and_alcoholic_preferences.white_wine_name
            quantity = guest.beverages_and_alcoholic_preferences.white_wine_quantity
        if alcohol_type == "Champagne":
            description = guest.beverages_and_alcoholic_preferences.champagne_name
            quantity = guest.beverages_and_alcoholic_preferences.champagne_quantity
        if description:
            writer.writerow(
                [
                    guest,
                    "Interior",
                    "Alcoholic",
                    alcohol_type,
                    description,
                    quantity,
                    "",
                ]
            )


def get_room_and_services(writer, guest, description, type, other):
    if other:
        if guest.diet_services_sizes_preferences.other_service.name:
            if "[" and "]" in guest.diet_services_sizes_preferences.other_service.name:
                for item in eval(
                    guest.diet_services_sizes_preferences.other_service.name
                ):
                    writer.writerow(
                        [
                            guest,
                            "Interior",
                            "Room & Services",
                            "Other Services",
                            dict(OTHER_SERVICES)[item],
                            "",
                            guest.diet_services_sizes_preferences.other_services_other_notes,
                        ]
                    )
    else:
        if description:
            writer.writerow(
                [
                    guest,
                    "Interior",
                    "Room & Services",
                    type,
                    description,
                ]
            )


def get_sizing_preferences(writer, guest, type, description):
    writer.writerow([guest, "Interior", "Sizing", type, description])


def get_dietary_restrictions(writer, guest):
    if (
        guest.diet_services_sizes_preferences.dietary_restrictions
        and guest.diet_services_sizes_preferences.dietary_restrictions != "NONE"
    ):
        writer.writerow(
            [
                guest,
                "Deck, Interior, Galley",
                "Dietary Restrictions",
                "Dietary Restrictions",
                guest.diet_services_sizes_preferences.get_dietary_restrictions_display(),
                "",
                guest.diet_services_sizes_preferences.dietary_restrictions_other_notes,
            ]
        )


def get_food_sensitivities(writer, guest):
    if guest.lactose_intolerant:
        writer.writerow(
            [
                guest,
                "Deck, Interior, Galley",
                "Food Sensitivities",
                "Food Sensitivities",
                "Lactose Intolerant",
                "",
                "",
            ]
        )
    if guest.shellfish_allergy:
        writer.writerow(
            [
                guest,
                "Deck, Interior, Galley",
                "Food Sensitivities",
                "Food Sensitivities",
                "Shellfish Allergy",
                "",
                "",
            ]
        )
    if guest.nut_allergy:
        writer.writerow(
            [
                guest,
                "Deck, Interior, Galley",
                "Food Sensitivities",
                "Food Sensitivities",
                "Nut Allergy",
                "",
                "",
            ]
        )
    if guest.gluten_free:
        writer.writerow(
            [
                guest,
                "Deck, Interior, Galley",
                "Food Sensitivities",
                "Food Sensitivities",
                "Gluten Free",
                "",
                "",
            ]
        )
    if guest.other:
        writer.writerow(
            [
                guest,
                "Deck, Interior, Galley",
                "Food Sensitivities",
                "Food Sensitivities",
                guest.other_notes,
                "",
                "",
            ]
        )


def extract_meal_times_and_types(charter, guest_list):
    # Preference Header
    HEADER = [
        "Guest Name",
        "Department",
        "Meal",
        "Time",
        "Meal Type",
        "Note to Chef",
    ]

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename={charter}-Meal.csv"

    writer = csv.writer(response, delimiter=",")
    writer.writerow(HEADER)

    for guest in guest_list:
        if guest.has_meal_and_room_pref:
            breakfast_selection = ""
            lunch_selection = ""
            dinner_selection = ""
            if "[" and "]" in guest.meal_and_room_preferences.breakfast_selection.name:
                for item in eval(
                    guest.meal_and_room_preferences.breakfast_selection.name
                ):
                    breakfast_selection += dict(BREAKFAST)[item] + ", "
            if "[" and "]" in guest.meal_and_room_preferences.lunch_selection.name:
                for item in eval(guest.meal_and_room_preferences.lunch_selection.name):
                    lunch_selection += dict(LUNCH)[item] + ", "
            if "[" and "]" in guest.meal_and_room_preferences.dinner_selection.name:
                for item in eval(guest.meal_and_room_preferences.dinner_selection.name):
                    dinner_selection += dict(DINNER)[item] + ", "
            writer.writerow(
                [
                    guest,
                    "Galley, Interior",
                    "Breakfast",
                    guest.meal_and_room_preferences.get_breakfast_time_display(),
                    breakfast_selection,
                    guest.meal_and_room_preferences.breakfast_note,
                ]
            )
            writer.writerow(
                [
                    "",
                    "Galley, Interior",
                    "Lunch",
                    guest.meal_and_room_preferences.get_lunch_time_display(),
                    lunch_selection,
                    guest.meal_and_room_preferences.lunch_note,
                ]
            )
            writer.writerow(
                [
                    "",
                    "Galley, Interior",
                    "Dinner",
                    guest.meal_and_room_preferences.get_dinner_time_display(),
                    dinner_selection,
                    guest.meal_and_room_preferences.dinner_note,
                ]
            )
            writer.writerow(
                [
                    "",
                    "Galley, Interior",
                    "Canapes",
                    guest.meal_and_room_preferences.get_canapes_time_display(),
                    guest.meal_and_room_preferences.get_canapes_selection_display(),
                    "",
                ]
            )
            writer.writerow(
                [
                    "",
                    "Galley, Interior",
                    "Mid-Morning Snack",
                    "-",
                    guest.meal_and_room_preferences.get_midmorning_snacks_display(),
                    "",
                ]
            )
            writer.writerow(
                [
                    "",
                    "Galley, Interior",
                    "Mid-Afternoon Snack",
                    "-",
                    guest.meal_and_room_preferences.get_midafternoon_snacks_display(),
                    "",
                ]
            )

    return response


# flake8: noqa: C901
def extract_preferences(charter, preferences_and_shopping_list, guest_list):
    # Preference Header
    HEADER = [
        "Guest Name",
        "Department",
        "Category",
        "Type",
        "Item Description",
        "Quantity",
        "Note to Crew",
    ]

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename={charter}.csv"

    # Create the CSV writer using the HttpResponse as the "file"
    writer = csv.writer(response, delimiter=",")
    writer.writerow(HEADER)

    if "FOOD_SENSITIVITES" in preferences_and_shopping_list:
        for guest in guest_list:
            get_food_sensitivities(writer, guest)
    if "DIETARY_RESTRICTIONS" in preferences_and_shopping_list:
        for guest in guest_list:
            if guest.has_diet_services_sizes_pref:
                get_dietary_restrictions(writer, guest)
    if "FOOD" in preferences_and_shopping_list:
        for guest in guest_list:
            if guest.has_food_pref:
                get_food_preferences(writer, guest)
    if "BEVERAGES" in preferences_and_shopping_list:
        for guest in guest_list:
            if guest.has_beverages_and_alcoholic_pref:
                get_beverages_preferences(writer, guest)
    if "ALCOHOLIC" in preferences_and_shopping_list:
        for guest in guest_list:
            if guest.has_beverages_and_alcoholic_pref:
                get_alcoholic_preferences(writer, guest)
    if "ROOM_AND_SERVICES" in preferences_and_shopping_list:
        for guest in guest_list:
            if guest.has_diet_services_sizes_pref:
                get_room_and_services(
                    writer,
                    guest,
                    guest.diet_services_sizes_preferences.favorite_flowers,
                    "Flowers",
                    "",
                )
                get_room_and_services(
                    writer,
                    guest,
                    guest.diet_services_sizes_preferences.preferred_room_temperature,
                    "Room Temperature",
                    "",
                )
                get_room_and_services(writer, guest, "", "Other Services", "other")
    if "SIZING" in preferences_and_shopping_list:
        for guest in guest_list:
            if guest.has_diet_services_sizes_pref:
                get_sizing_preferences(
                    writer,
                    guest,
                    "Shirt Size",
                    f"{guest.diet_services_sizes_preferences.get_shirt_sizing_display()}, {guest.diet_services_sizes_preferences.get_international_shirt_sizing_display()}, {guest.diet_services_sizes_preferences.get_shirt_size_display()}",
                )
                get_sizing_preferences(
                    writer,
                    guest,
                    "Shoe Size",
                    f"{guest.diet_services_sizes_preferences.get_shoe_sizing_display()}, {guest.diet_services_sizes_preferences.get_international_shoe_sizing_display()}, {guest.diet_services_sizes_preferences.shoe_size}",
                )

    return response


def generate_guest_details_pdf(request, guest, charter):

    breakfast_selection = None
    lunch_selection = None
    dinner_selection = None
    other_services = None
    milk_selection = None
    coffee_selection = None
    tea_selection = None
    water_selection = None
    juice_selection = None
    sodas_and_mixers_selection = None
    add_ons_selection = None

    meal_and_room_preferences = (
        guest.meal_and_room_preferences
        if hasattr(guest, "meal_and_room_preferences")
        else None
    )
    if meal_and_room_preferences:
        breakfast_selection = meal_and_room_preferences.breakfast_selection
        lunch_selection = meal_and_room_preferences.lunch_selection
        dinner_selection = meal_and_room_preferences.dinner_selection

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

    beverages_and_alcoholic_preferences = (
        guest.beverages_and_alcoholic_preferences
        if hasattr(guest, "beverages_and_alcoholic_preferences")
        else None
    )

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
        "breakfast_selection": breakfast_selection.name,
        "lunch_selection": lunch_selection.name,
        "dinner_selection": dinner_selection.name,
        "other_services": other_services.name
        if hasattr(other_services, "name")
        else None,
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

    html_string = render_to_string(
        "charter/pdf/guest_details.html",
        ctx,
    )
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf(
        stylesheets=[
            CSS("authentication" + settings.STATIC_URL + "authentication/css/main.css")
        ]
    )

    response = HttpResponse(content_type="application/pdf;")
    response["Content-Disposition"] = f"attachment; filename={guest}.pdf"

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())

    return response


def generate_short_jet_pdf(request: HttpRequest, guest: GuestDetail):
    ctx = {
        "guest": guest,
        "preference": guest.short_jet_preference,
    }

    html_string = render_to_string(
        "preferences/pdf/short_jet_preference.html",
        ctx,
    )
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf(
        stylesheets=[
            CSS("authentication" + settings.STATIC_URL + "authentication/css/main.css")
        ]
    )

    response = HttpResponse(content_type="application/pdf;")
    response[
        "Content-Disposition"
    ] = f"attachment; filename={guest.first_name.title()} {guest.last_name.title()} - Short Jet Preference.pdf"

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())

    return response


def generate_long_jet_pdf(request: HttpRequest, guest: GuestDetail):
    ctx = {
        "guest": guest,
        "preference": guest.long_jet_preference,
    }

    html_string = render_to_string(
        "preferences/pdf/long_jet_preference.html",
        ctx,
    )
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf(
        stylesheets=[
            CSS("authentication" + settings.STATIC_URL + "authentication/css/main.css")
        ]
    )

    response = HttpResponse(content_type="application/pdf;")
    response[
        "Content-Disposition"
    ] = f"attachment; filename={guest.first_name.title()} {guest.last_name.title()} - Long Jet Preferences.pdf"

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())

    return response


def generate_trip_details_pdf(request, charter):
    guest_list = []
    guest_list.insert(0, charter.principal_guest)
    for guest in charter.guests.all():
        guest_list.append(guest)

    ctx = {
        "charter": charter,
        "principal": charter.principal_guest,
        "guests": guest_list,
    }

    html_string = render_to_string(
        "charter/pdf/trip_details.html",
        ctx,
    )
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf(
        stylesheets=[
            CSS("authentication" + settings.STATIC_URL + "authentication/css/main.css")
        ]
    )

    response = HttpResponse(content_type="application/pdf;")
    response["Content-Disposition"] = f"attachment; filename={charter}.pdf"

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())

    return response


def generate_meal_times_and_types_pdf(request, data):

    html_string = render_to_string(
        "charter/pdf/meal_times_and_types.html",
        data,
    )
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf(
        stylesheets=[
            CSS("authentication" + settings.STATIC_URL + "authentication/css/main.css")
        ]
    )
    response = HttpResponse(content_type="application/pdf;")
    response[
        "Content-Disposition"
    ] = f"attachment; filename=meal_times_&_types-{data.get('charter')}.pdf"

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())

    return response


def send_email_template(*, subject, recipients: list, template, data, is_secure=False):
    """
    This function sends an email using a selected template.

    Sends a trip invite to the given list of emails.
    Returns whether the email has been sent or not.

    Arguments:
        subject: the subject of the email
        recipients: a list of recipients the email will be sent to
        template: the template to be used for the email
        data: a dictionary to be added as context variables in the email
    """
    try:
        domain = Site.objects.get_current().domain
        protocol = "https" if is_secure else "http"
        context = {
            "guest_register_url": GUEST_REGISTER_URL,
            "site": f"{protocol}://{domain}",
        }
        context.update(data)

        html_content = render_to_string(template, context)
        text_content = strip_tags(html_content)

        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.EMAIL_FROM,
            recipient_list=recipients,
            fail_silently=False,
            html_message=html_content,
        )
        return True
    except Exception as err:
        print(err)


def context_helper():
    from authentication.models import User
    from charter.models import Charter

    user: User = User.objects.get(id=2)
    charter: Charter = Charter.objects.get(id=2)
    guest_list = list(charter.guests.all().order_by("id"))
    guest_list.insert(0, charter.principal_guest)

    return {
        "user": user,
        "charter": charter,
        "breadcrumbs": f"Dashboard > Itinerary > {charter}",
        "active": "guests",
        "vessel": charter.vessel,
        "guests": guest_list,
        "principal_guest": charter.principal_guest,
        "guests_email": [guest.email for guest in guest_list],
    }


def get_shopping_list_response(
    request: HttpRequest,
    charter: Charter,
    preference_list: list[str],
) -> HttpResponse:
    preferences, preferences_notes = food_preferences_shopping_list(charter)
    beverages, beverage_notes = beverage_preferences_shopping_list(charter)
    food_choices = [
        "General Cuisine",
        "Fish And Shellfish",
        "Meat",
        "Bread",
        "Soup",
        "Salad",
        "Cheese",
        "Dessert",
        "Kids Meals",
    ]
    ctx = {
        "charter": charter,
        "preferences": preferences,
        "preferences_notes": preferences_notes,
        "beverages": beverages,
        "beverage_notes": beverage_notes,
        "preference_list": preference_list,
        "food_choices": food_choices,
        "alcohols": alcohol_preferences_shopping_list(charter)
        if "ALCOHOLIC" in preference_list
        else {},
        "guests": charter.guests.all(),
    }

    html_string = render_to_string(
        "charter/pdf/shopping_list.html",
        ctx,
    )
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf(
        stylesheets=[
            CSS("authentication" + settings.STATIC_URL + "authentication/css/main.css")
        ]
    )

    response = HttpResponse(content_type="application/pdf;")
    response[
        "Content-Disposition"
    ] = f"attachment; filename=Shopping List - {charter}.pdf"

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())

    return response


def get_crew_profile_response(
    request: HttpRequest,
    crew: CrewProfile,
) -> HttpResponse:
    ctx = {"crew": crew}
    html_string = render_to_string(
        "charter/pdf/crew_profile.html",
        ctx,
    )
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf(
        stylesheets=[CSS("core" + settings.STATIC_URL + "core/css/crew_profile.css")]
    )

    response = HttpResponse(content_type="application/pdf;")
    response[
        "Content-Disposition"
    ] = f"attachment; filename={crew.name} - Crew Profile.pdf"

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())

    return response
