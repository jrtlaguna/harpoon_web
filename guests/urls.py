from django.urls import path

from guests import views
from guests import views_2

app_name = "guests"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile_settings, name="profile"),
    path(
        "dashboard/settings/change_password/",
        views.settings_change_password,
        name="settings_change_password",
    ),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path(
        "forgot_password_code/<str:email>/",
        views.forgot_password_code,
        name="forgot_password_code",
    ),
    path(
        "resend_password_code/<str:email>/",
        views.resend_password_code,
        name="resend_password_code",
    ),
    path(
        "change_password/<str:email>/<str:code>/",
        views.change_password,
        name="change_password",
    ),
    path(
        "trips/",
        views.trips,
        name="trips",
    ),
    path(
        "trips/<int:charter_id>/",
        views.trip_details,
        name="trip_details",
    ),
    path(
        "onboarding_profile/",
        views.onboarding_profile,
        name="profile_onboarding",
    ),
    path(
        "onboarding_yacht_food/",
        views.onboarding_yacht_food,
        name="yacht_food_onboarding",
    ),
    path(
        "onboarding_meals_and_room/",
        views.onboarding_meals_room,
        name="onboarding_meals_and_room",
    ),
    path(
        "onboarding_diet_services/",
        views.onboarding_diet_services,
        name="onboarding_diet_services",
    ),
    path(
        "onboarding_beverages/",
        views.onboarding_beverages,
        name="onboarding_beverages",
    ),
    path(
        "profile_picture_upload/",
        views.profile_image_upload,
        name="profile_image_upload",
    ),
    path(
        "upload_documents/",
        views.upload_documents,
        name="document_upload",
    ),
    path(
        "download_passport/",
        views.download_passport,
        name="download_passport",
    ),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path(
        "terms_and_conditions/", views.terms_and_conditions, name="terms_and_conditions"
    ),
    path("ver2/dashboard/", views_2.dashboard, name="dashboard-2"),
]
