import ast
from datetime import datetime

from django.db.models import F, QuerySet

from charter.models import Charter, GuestDetail


def food_preferences_shopping_list(charter: Charter):
    food_dict = {
        "general_cuisine": F("food_preferences__general_cuisine"),
        "fish_and_shellfish": F("food_preferences__fish_and_shellfish"),
        "meat": F("food_preferences__meat"),
        "bread": F("food_preferences__bread"),
        "salad": F("food_preferences__salad"),
        "soup": F("food_preferences__soup"),
        "cheese": F("food_preferences__cheese"),
        "dessert": F("food_preferences__dessert"),
        "kids_meals": F("food_preferences__dessert"),
    }
    food_notes_dict = {
        "general_cuisine": F("food_preferences__general_cuisine_notes"),
        "fish_and_shellfish": F("food_preferences__fish_and_shellfish_notes"),
        "meat": F("food_preferences__meat_notes"),
        "bread": F("food_preferences__bread_notes"),
        "salad": F("food_preferences__salad_notes"),
        "soup": F("food_preferences__soup_notes"),
        "cheese": F("food_preferences__cheese_notes"),
        "dessert": F("food_preferences__dessert_notes"),
        "kids_meals": F("food_preferences__kids_meals_notes"),
        "kids_allergies": F("food_preferences__kids_allergies"),
        "first": F("first_name"),
        "last": F("last_name"),
    }
    guests_notes = charter.guests.filter(food_preferences__isnull=False).values(
        **food_notes_dict
    )
    guests = charter.guests.filter(food_preferences__isnull=False).values(
        **food_dict,
    )
    food_results = dict()

    for key in food_dict.keys():
        food_results[key] = parse_string_to_list(key, guests)

    notes_result = dict()
    for key in food_notes_dict.keys():
        modified_key = key.replace("_", " ").title()
        result = parse_notes_to_list(key, guests_notes)
        if result == []:
            continue
        notes_result[modified_key] = result
    return food_results, notes_result


def parse_string_to_list(key, guests):
    result = dict()
    for guest in guests:
        literal = ast.literal_eval(guest.get(key, "[]"))
        for food in literal:
            modified_key = food.replace("_", " ").title()
            if modified_key in result.keys():
                result[modified_key] += 1
            else:
                result[modified_key] = 1
    return result


def parse_notes_to_list(key, guests):

    result = []
    for guest in guests:
        if guest.get(key) not in [None, ""]:
            guest_name = f"{guest.get('first')} {guest.get('last')}"
            note = f"{guest.get(key)}"
            if guest.get("first"):
                note = f"{note} - {guest_name}"
            result.append(note)
    return result


def beverage_preferences_shopping_list(charter: Charter):
    bev_dict = {
        "milk": F("beverages_and_alcoholic_preferences__milk_selection__name"),
        "coffee": F("beverages_and_alcoholic_preferences__coffee_selection__name"),
        "tea": F("beverages_and_alcoholic_preferences__tea_selection__name"),
        "water": F("beverages_and_alcoholic_preferences__water_selection__name"),
        "juice": F("beverages_and_alcoholic_preferences__juice_selection__name"),
        "sodas_and_mixers": F(
            "beverages_and_alcoholic_preferences__sodas_and_mixers_selection__name"
        ),
        "add_ons": F("beverages_and_alcoholic_preferences__add_ons_selection__name"),
    }
    bev_notes_dict = {
        "milk": F("beverages_and_alcoholic_preferences__milk_note"),
        "coffee": F("beverages_and_alcoholic_preferences__coffee_note"),
        "tea": F("beverages_and_alcoholic_preferences__tea_note"),
        "water": F("beverages_and_alcoholic_preferences__water_note"),
        "juice": F("beverages_and_alcoholic_preferences__juice_note"),
        "sodas_and_mixers": F(
            "beverages_and_alcoholic_preferences__sodas_and_mixers_note"
        ),
        "add_ons": F("beverages_and_alcoholic_preferences__add_ons_note"),
        "first": F("first_name"),
        "last": F("last_name"),
    }

    guests_notes = charter.guests.filter(
        beverages_and_alcoholic_preferences__isnull=False
    ).values(**bev_notes_dict)
    guests = charter.guests.filter(
        beverages_and_alcoholic_preferences__isnull=False
    ).values(
        **bev_dict,
    )

    bev_results = dict()

    for key in bev_dict.keys():
        bev_results[key] = parse_string_to_list(key, guests)

    notes_result = dict()
    for key in bev_notes_dict.keys():
        modified_key = key.replace("_", " ").title()
        result = parse_notes_to_list(key, guests_notes)
        if result == []:
            continue
        notes_result[modified_key] = result

    return bev_results, notes_result


def alcohol_preferences_shopping_list(charter: Charter):  # noqa: C901
    alcohol_dict = {
        "whiskey_name": F("beverages_and_alcoholic_preferences__whiskey_name"),
        "brandy_name": F("beverages_and_alcoholic_preferences__brandy_name"),
        "vodka_name": F("beverages_and_alcoholic_preferences__vodka_name"),
        "tequila_name": F("beverages_and_alcoholic_preferences__tequila_name"),
        "rum_name": F("beverages_and_alcoholic_preferences__rum_name"),
        "liquors_name": F("beverages_and_alcoholic_preferences__liquors_name"),
        "cocktail_name": F("beverages_and_alcoholic_preferences__cocktail_name"),
        "port_beer_name": F("beverages_and_alcoholic_preferences__port_beer_name"),
        "red_wine_name": F("beverages_and_alcoholic_preferences__red_wine_name"),
        "white_wine_name": F("beverages_and_alcoholic_preferences__white_wine_name"),
        "rose_wine_name": F("beverages_and_alcoholic_preferences__rose_wine_name"),
        "champagne_name": F("beverages_and_alcoholic_preferences__champagne_name"),
        "other_name": F("beverages_and_alcoholic_preferences__other_name"),
        "whiskey_quantity": F("beverages_and_alcoholic_preferences__whiskey_quantity"),
        "brandy_quantity": F("beverages_and_alcoholic_preferences__brandy_quantity"),
        "vodka_quantity": F("beverages_and_alcoholic_preferences__vodka_quantity"),
        "tequila_quantity": F("beverages_and_alcoholic_preferences__tequila_quantity"),
        "rum_quantity": F("beverages_and_alcoholic_preferences__rum_quantity"),
        "liquors_quantity": F("beverages_and_alcoholic_preferences__liquors_quantity"),
        "cocktail_quantity": F(
            "beverages_and_alcoholic_preferences__cocktail_quantity"
        ),
        "port_beer_quantity": F(
            "beverages_and_alcoholic_preferences__port_beer_quantity"
        ),
        "red_wine_quantity": F(
            "beverages_and_alcoholic_preferences__red_wine_quantity"
        ),
        "white_wine_quantity": F(
            "beverages_and_alcoholic_preferences__white_wine_quantity"
        ),
        "rose_wine_quantity": F(
            "beverages_and_alcoholic_preferences__rose_wine_quantity"
        ),
        "champagne_quantity": F(
            "beverages_and_alcoholic_preferences__champagne_quantity"
        ),
        "extra_whiskey": F("beverages_and_alcoholic_preferences__extra_whiskey"),
        "extra_brandy": F("beverages_and_alcoholic_preferences__extra_brandy"),
        "extra_vodka": F("beverages_and_alcoholic_preferences__extra_vodka"),
        "extra_tequila": F("beverages_and_alcoholic_preferences__extra_tequila"),
        "extra_rum": F("beverages_and_alcoholic_preferences__extra_rum"),
        "extra_liquors": F("beverages_and_alcoholic_preferences__extra_liquors"),
        "extra_cocktail": F("beverages_and_alcoholic_preferences__extra_cocktail"),
        "extra_port_beer": F("beverages_and_alcoholic_preferences__extra_port_beer"),
        "extra_red_wine": F("beverages_and_alcoholic_preferences__extra_red_wine"),
        "extra_white_wine": F("beverages_and_alcoholic_preferences__extra_white_wine"),
        "extra_rose_wine": F("beverages_and_alcoholic_preferences__extra_rose_wine"),
        "extra_champagne": F("beverages_and_alcoholic_preferences__extra_champagne"),
        "other_quantity": F("beverages_and_alcoholic_preferences__other_quantity"),
    }

    qs = charter.guests.filter(
        beverages_and_alcoholic_preferences__isnull=False
    ).values(**alcohol_dict)

    whiskey = dict()
    brandy = dict()
    vodka = dict()
    tequila = dict()
    rum = dict()
    liquors = dict()
    cocktail = dict()
    port_beer = dict()
    red_wine = dict()
    white_wine = dict()
    rose_wine = dict()
    champagne = dict()
    for guest in qs:
        if guest.get("whiskey_name"):
            whiskey_key = guest.get("whiskey_name").replace("_", " ").title()
            if guest.get("whiskey_name") in whiskey.keys():
                whiskey[whiskey_key] += guest.get("whiskey_quantity")
            else:
                whiskey[whiskey_key] = guest.get("whiskey_quantity")
        if guest.get("extra_whiskey"):
            for key, value in guest.get("extra_whiskey").items():
                whiskey_key = key.replace("_", " ").title()
                if whiskey_key in whiskey.keys():
                    whiskey[whiskey_key] += int(value) if value else 0
                else:
                    whiskey[whiskey_key] = int(value) if value else 0

        # DIVIDER
        if guest.get("brandy_name"):
            brandy_key = guest.get("brandy_name").replace("_", " ").title()
            if guest.get("brandy_name") in brandy.keys():
                brandy[brandy_key] += guest.get("brandy_quantity")
            else:
                brandy[brandy_key] = guest.get("brandy_quantity")
        if guest.get("extra_brandy"):
            for key, value in guest.get("extra_brandy").items():
                brandy_key = key.replace("_", " ").title()
                if brandy_key in brandy.keys():
                    brandy[brandy_key] += int(value) if value else 0
                else:
                    brandy[brandy_key] = int(value) if value else 0

        # DIVIDER
        if guest.get("vodka_name"):
            vodka_key = guest.get("vodka_name").replace("_", " ").title()
            if guest.get("vodka_name") in vodka.keys():
                vodka[vodka_key] += guest.get("vodka_quantity")
            else:
                vodka[vodka_key] = guest.get("vodka_quantity")
        if guest.get("extra_vodka"):
            for key, value in guest.get("extra_vodka").items():
                vodka_key = key.replace("_", " ").title()
                if vodka_key in vodka.keys():
                    vodka[vodka_key] += int(value) if value else 0
                else:
                    vodka[vodka_key] = int(value) if value else 0

        # DIVIDER
        if guest.get("tequila_name"):
            tequila_key = guest.get("tequila_name").replace("_", " ").title()
            if guest.get("tequila_name") in tequila.keys():
                tequila[tequila_key] += guest.get("tequila_quantity")
            else:
                tequila[tequila_key] = guest.get("tequila_quantity")
        if guest.get("extra_tequila"):
            for key, value in guest.get("extra_tequila").items():
                tequila_key = key.replace("_", " ").title()
                if tequila_key in tequila.keys():
                    tequila[tequila_key] += int(value) if value else 0
                else:
                    tequila[tequila_key] = int(value) if value else 0

        # DIVIDER
        if guest.get("rum_name"):
            rum_key = guest.get("rum_name").replace("_", " ").title()
            if guest.get("rum_name") in rum.keys():
                rum[rum_key] += guest.get("rum_quantity")
            else:
                rum[rum_key] = guest.get("rum_quantity")
        if guest.get("extra_rum"):
            for key, value in guest.get("extra_rum").items():
                rum_key = key.replace("_", " ").title()
                if rum_key in rum.keys():
                    rum[rum_key] += int(value) if value else 0
                else:
                    rum[rum_key] = int(value) if value else 0

        # DIVIDER
        if guest.get("liquors_name"):
            liquors_key = guest.get("liquors_name").replace("_", " ").title()
            if guest.get("liquors_name") in liquors.keys():
                liquors[liquors_key] += guest.get("liquors_quantity")
            else:
                liquors[liquors_key] = guest.get("liquors_quantity")
        if guest.get("extra_liquors"):
            for key, value in guest.get("extra_liquors").items():
                liquors_key = key.replace("_", " ").title()
                if liquors_key in liquors.keys():
                    liquors[liquors_key] += int(value) if value else 0
                else:
                    liquors[liquors_key] = int(value) if value else 0

        # DIVIDER
        if guest.get("cocktail_name"):
            cocktail_key = guest.get("cocktail_name").replace("_", " ").title()
            if guest.get("cocktail_name") in cocktail.keys():
                cocktail[cocktail_key] += guest.get("cocktail_quantity")
            else:
                cocktail[cocktail_key] = guest.get("cocktail_quantity")
        if guest.get("extra_cocktail"):
            for key, value in guest.get("extra_cocktail").items():
                cocktail_key = key.replace("_", " ").title()
                if cocktail_key in cocktail.keys():
                    cocktail[cocktail_key] += int(value) if value else 0
                else:
                    cocktail[cocktail_key] = int(value) if value else 0

        # DIVIDER
        if guest.get("port_beer_name"):
            port_beer_key = guest.get("port_beer_name").replace("_", " ").title()
            if guest.get("port_beer_name") in port_beer.keys():
                port_beer[port_beer_key] += guest.get("port_beer_quantity")
            else:
                port_beer[port_beer_key] = guest.get("port_beer_quantity")
        if guest.get("extra_port_beer"):
            for key, value in guest.get("extra_port_beer").items():
                port_beer_key = key.replace("_", " ").title()
                if port_beer_key in port_beer.keys():
                    port_beer[port_beer_key] += int(value) if value else 0
                else:
                    port_beer[port_beer_key] = int(value) if value else 0

        # DIVIDER
        if guest.get("red_wine_name"):
            red_wine_key = guest.get("red_wine_name").replace("_", " ").title()
            if guest.get("red_wine_name") in red_wine.keys():
                red_wine[red_wine_key] += guest.get("red_wine_quantity")
            else:
                red_wine[red_wine_key] = guest.get("red_wine_quantity")
        if guest.get("extra_red_wine"):
            for key, value in guest.get("extra_red_wine").items():
                red_wine_key = key.replace("_", " ").title()
                if red_wine_key in red_wine.keys():
                    red_wine[red_wine_key] += int(value) if value else 0
                else:
                    red_wine[red_wine_key] = int(value) if value else 0

        # DIVIDER
        if guest.get("white_wine_name"):
            white_wine_key = guest.get("white_wine_name").replace("_", " ").title()
            if guest.get("white_wine_name") in white_wine.keys():
                white_wine[white_wine_key] += guest.get("white_wine_quantity")
            else:
                white_wine[white_wine_key] = guest.get("white_wine_quantity")
        if guest.get("extra_white_wine"):
            for key, value in guest.get("extra_white_wine").items():
                white_wine_key = key.replace("_", " ").title()
                if white_wine_key in white_wine.keys():
                    white_wine[white_wine_key] += int(value) if value else 0
                else:
                    white_wine[white_wine_key] = int(value) if value else 0

        # DIVIDER
        if guest.get("rose_wine_name"):
            rose_wine_key = guest.get("rose_wine_name").replace("_", " ").title()
            if guest.get("rose_wine_name") in rose_wine.keys():
                rose_wine[rose_wine_key] += guest.get("rose_wine_quantity")
            else:
                rose_wine[rose_wine_key] = guest.get("rose_wine_quantity")
        if guest.get("extra_rose_wine"):
            for key, value in guest.get("extra_rose_wine").items():
                rose_wine_key = key.replace("_", " ").title()
                if rose_wine_key in rose_wine.keys():
                    rose_wine[rose_wine_key] += int(value) if value else 0
                else:
                    rose_wine[rose_wine_key] = int(value) if value else 0

        # DIVIDER
        if guest.get("champagne_name"):
            champagne_key = guest.get("champagne_name").replace("_", " ").title()
            if guest.get("champagne_name") in champagne.keys():
                champagne[champagne_key] += guest.get("champagne_quantity")
            else:
                champagne[champagne_key] = guest.get("champagne_quantity")
        if guest.get("extra_champagne"):
            for key, value in guest.get("extra_champagne").items():
                champagne_key = key.replace("_", " ").title()
                if champagne_key in champagne.keys():
                    champagne[champagne_key] += int(value) if value else 0
                else:
                    champagne[champagne_key] = int(value) if value else 0

    result = {
        "Whiskey": whiskey,
        "Brandy": brandy,
        "Vodka": vodka,
        "Tequila": tequila,
        "Rum": rum,
        "Liquors": liquors,
        "Cocktail": cocktail,
        "Port Beer": port_beer,
        "Red Wine": red_wine,
        "White Wine": white_wine,
        "Rose Wine": rose_wine,
        "Champagne": champagne,
    }
    return result
