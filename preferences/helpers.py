from typing import List
from datetime import datetime
import pytz


def get_max_pref_created_date(guest):

    pref_created_date_list = []
    if guest.has_food_pref:
        pref_created_date_list.append(guest.food_preferences.created_at)
        pref_created_date_list.append(guest.food_preferences.updated_at)

    if guest.has_meal_and_room_pref:
        pref_created_date_list.append(guest.meal_and_room_preferences.created_at)
        pref_created_date_list.append(guest.meal_and_room_preferences.updated_at)

    if guest.has_diet_services_sizes_pref:
        pref_created_date_list.append(guest.diet_services_sizes_preferences.created_at)
        pref_created_date_list.append(guest.diet_services_sizes_preferences.updated_at)

    if guest.has_beverages_and_alcoholic_pref:
        pref_created_date_list.append(
            guest.beverages_and_alcoholic_preferences.created_at
        )
        pref_created_date_list.append(
            guest.beverages_and_alcoholic_preferences.updated_at
        )

    now = datetime.now(pytz.utc)
    latest = ""
    if pref_created_date_list:
        latest = max(dt for dt in pref_created_date_list if dt < now)

    return latest


def get_additional_alcohol(alcohol_type: str, response_data: dict) -> dict:
    res = {}
    keys = []
    for key in response_data.keys():
        if key.startswith(f"{alcohol_type}_name") and not key.endswith("name"):
            keys.append(key.split("_")[-1])
    for key in keys:
        quantity = response_data.get(f"{alcohol_type}_quantity_{key}")
        name = response_data.get(f"{alcohol_type}_name_{key}")
        if quantity not in ["", None, "0"] and name not in ["", None, "0"]:
            res[name] = quantity

    return res


def generate_html_from_alcohol_dict(alcohol_type, alcohol_dict) -> str:
    htmls = ""
    count = 0
    for name, value in alcohol_dict.items():
        htmls += define_html_alcohol(alcohol_type, name, value, count)
    return htmls


def define_html_alcohol(alcohol_type: str, name: str, value: int, count: int) -> str:
    html = f"""
        <div class="col-12 mb-1 d-flex flex-column">
            <div class="col-12 d-flex align-items-end">
                <div class="form-group py-0 w-100">
                    <input type="text" class="form-control" name="{alcohol_type}_name_{count}" id="id_{alcohol_type}_name" value="{name}" placeholder="Brand, Color, Vineyard / Region">
                </div>

                <div class="input-group inc pb-3 px-3">
                    <div class="input-group-prepend">
                        <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="minus_bev">
                            <span class="material-icons fs-25 txt-color-gold">remove_circle</span> </button>
                    </div>

                    <input type="text" class="form-control form-input text-center bg-transparent border-0 p-0" placeholder="0"
                        name="{alcohol_type}_quantity_{count}" value="{value}" id="ind_bev">

                    <div class="input-group-append">
                        <button type="button" class="px-0 btn btn-sm bg-transparent d-flex align-items-center" id="add_bev">
                            <span class="material-icons fs-25 txt-color-gold">add_circle</span> </button>
                    </div>
                </div>
            </div>
        </div>
    """
    return html
