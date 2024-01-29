from django.urls import path

from charter import views

app_name = "charter"

urlpatterns = [
    path("<int:charter_id>/", views.trip_details, name="trip_details"),
    path(
        "new_trip/",
        views.new_trip,
        name="new_trip",
    ),
    path(
        "<int:charter_id>/charter_details/",
        views.charter_details,
        name="charter_details",
    ),
    path(
        "<int:vessel_id>/new_trip_details/",
        views.new_trip_details,
        name="new_trip_details",
    ),
    path(
        "<int:charter_id>/charter_locations/",
        views.add_charter_locations,
        name="charter_locations",
    ),
    path("<int:charter_id>/add_guests/", views.add_guests, name="add_guests"),
    path(
        "<int:charter_id>/review_and_submit/",
        views.review_and_submit,
        name="review_and_submit",
    ),
    path("<int:charter_id>/success/", views.charter_success, name="charter_success"),
    path("<int:charter_id>/guests/", views.guests, name="guests"),
    path(
        "<int:charter_id>/preferences_and_shopping_list/",
        views.preferences_and_shopping_list,
        name="preferences_and_shopping_list",
    ),
    path(
        "<int:charter_id>/guests/<int:guest_id>/",
        views.guest_details,
        name="guest_details",
    ),
    path(
        "<int:charter_id>/guests/<int:guest_id>/delete/",
        views.delete_guest,
        name="delete_guest",
    ),
    path(
        "<int:charter_id>/guests/<int:guest_id>/food_preferences/",
        views.guest_food_preferences,
        name="guest_food_preferences",
    ),
    path(
        "<int:charter_id>/guests/<int:guest_id>/meal_and_room_preferences/",
        views.guest_meal_and_room_preferences,
        name="guest_meal_and_room_preferences",
    ),
    path(
        "<int:charter_id>/guests/<int:guest_id>/diet_services_sizing/",
        views.guest_diet_services_sizing,
        name="guest_diet_services_sizing",
    ),
    path(
        "<int:charter_id>/guests/<int:guest_id>/beverage_alcohol/",
        views.guest_beverage_alcohol,
        name="guest_beverage_alcohol",
    ),
    path(
        "all_trips/",
        views.all_trips,
        name="all_trips",
    ),
    path(
        "<int:charter_id>/trip_details/",
        views.guest_trip_details,
        name="guest_trip_details",
    ),
    path(
        "<int:charter_id>/trip_details/edit/",
        views.edit_trip_details,
        name="edit_trip_details",
    ),
    path(
        "<int:charter_id>/download_meal_time_and_types/",
        views.download_meal_times_and_types,
        name="download_meal_times_and_types",
    ),
    path(
        "<int:charter_id>/download_shopping_list/",
        views.download_shopping_list,
        name="download_shopping_list",
    ),
]
