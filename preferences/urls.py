from django.urls import path

from preferences import views

app_name = "preferences"

urlpatterns = [
    path(
        "food/",
        views.food_preferences,
        name="food_preferences",
    ),
    path(
        "yacht-food/",
        views.yacht_food_preference,
        name="yacht_food_preference",
    ),
    path(
        "meal-and-room/",
        views.meal_and_room_preferences,
        name="meal_and_room_preferences",
    ),
    path(
        "diet-services-sizing/",
        views.diet_services_sizing,
        name="diet_services_sizing",
    ),
    path(
        "beverage-and-alcohol/",
        views.beverage_alcohol,
        name="beverage_alcohol",
    ),
    path(
        "download-preferences-pdf/",
        views.download_preferences_pdf,
        name="download_preferences_pdf",
    ),
    path(
        "download-short-jet-preferences/",
        views.download_short_jet_preferences,
        name="download_short_jet_preferences",
    ),
    path(
        "download-long-jet-preferences/",
        views.download_long_jet_preferences,
        name="download_long_jet_preferences",
    ),
    path(
        "short-jet/",
        views.short_jet_preference,
        name="short_jet_preference",
    ),
    path(
        "long-jet/",
        views.long_jet_preference,
        name="long_jet_preference",
    ),
    path(
        "add-new-alcohol/<str:alcohol_type>/",
        views.add_new_alcohol,
        name="add_new_alcohol",
    ),
]
