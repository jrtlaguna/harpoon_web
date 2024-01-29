from ast import literal_eval
from django import template

from preferences.constants import (
    ADD_ONS_SELECTIONS,
    BREAD,
    BREAKFAST,
    CHEESE,
    COFFEE_SELECTIONS,
    DESSERT,
    DIETARY_RESTRICTIONS,
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
    WATER_SELECTIONS,
)

register = template.Library()


@register.filter
def get_string_as_list(value):
    """Evaluate a string if it contains []"""
    if "[" and "]" in value:
        return eval(value)


def choices(text_choice):
    switcher = {
        "GENERAL_CUISINE": GENERAL_CUISINE,
        "FISH_SHELLFISH": FISH_SHELLFISH,
        "MEAT": MEAT,
        "BREAD": BREAD,
        "SOUP": SOUP,
        "SALAD": SALAD,
        "CHEESE": CHEESE,
        "DESSERT": DESSERT,
        "BREAKFAST": BREAKFAST,
        "LUNCH": LUNCH,
        "DINNER": DINNER,
        "DIETARY_RESTRICTIONS": DIETARY_RESTRICTIONS,
        "OTHER_SERVICES": OTHER_SERVICES,
        "MILK_SELECTIONS": MILK_SELECTIONS,
        "COFFEE_SELECTIONS": COFFEE_SELECTIONS,
        "TEA_SELECTIONS": TEA_SELECTIONS,
        "WATER_SELECTIONS": WATER_SELECTIONS,
        "JUICE_SELECTIONS": JUICE_SELECTIONS,
        "SODAS_MIXERS_SELECTIONS": SODAS_MIXERS_SELECTIONS,
        "ADD_ONS_SELECTIONS": ADD_ONS_SELECTIONS,
    }
    return switcher.get(text_choice, "Invalid text choice")


@register.filter
def get_display_name(val, arg):
    for choice in choices(arg):
        if choice[0] == val:
            return choice[1]
    return ""


@register.filter
def get_preference_display_name(val: str):
    return val.replace("_", " ").title()


@register.filter
def dict_to_list(dictionary, key):
    return dictionary.get(key)


@register.filter
def has_no_values(dictionary: dict):
    return len(dictionary.keys()) == 0 or all(val == 0 for val in dictionary.values())


@register.filter
def dict_value(dictionary, key):
    return dictionary.get(key)


@register.filter
def in_list(str_list: list[str], value: str):
    return value.upper() in str_list


@register.filter
def list_to_string(str_list):
    return ", ".join(str_list)


@register.filter
def string_to_list(string):
    try:
        new_list = literal_eval(string)
        return new_list
    except Exception as err:
        print(err)
        return ""


@register.filter
def string_list_to_string(str_list: str):
    try:
        string = literal_eval(str_list)
        formatted = ", ".join(string)
        return formatted.replace("_", " ").title()
    except Exception as err:
        print(err)
        return str_list if len(str_list) > 0 else ""
