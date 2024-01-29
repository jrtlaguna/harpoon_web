from django.urls import path

from admins import views

app_name = "admins"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/settings/", views.settings, name="settings"),
    path(
        "dashboard/settings/change_password/",
        views.settings_change_password,
        name="settings_change_password",
    ),
    path("register/", views.register, name="register"),
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
        "seen_notifications/",
        views.seen_notifications,
        name="seen_notifications",
    ),
    path(
        "search/",
        views.search,
        name="search",
    ),
    path(
        "guest-search/<int:guest_id>/",
        views.guest_search,
        name="guest_search",
    ),
    path(
        "privacy_policy/",
        views.privacy_policy,
        name="privacy_policy",
    ),
    path(
        "add-previous-yacht/",
        views.add_previous_yacht,
        name="add_previous_yacht",
    ),
    path(
        "crew-profile-list/",
        views.crew_profile_list,
        name="crew_profile_list",
    ),
    path(
        "crew-profile-create/",
        views.crew_profile_create,
        name="crew_profile_create",
    ),
    path(
        "<int:crew_id>/crew-profile-edit/",
        views.crew_profile_edit,
        name="crew_profile_edit",
    ),
    path(
        "<int:crew_id>/crew-profile-image-upload/",
        views.crew_profile_image_upload,
        name="crew_profile_image_upload",
    ),
    path(
        "<int:crew_id>/crew-profile-delete/",
        views.crew_profile_delete,
        name="crew_profile_delete",
    ),
    path(
        "<int:crew_id>/crew-profile-print/",
        views.crew_profile_print,
        name="crew_profile_print",
    ),
    path(
        "guest-info-list/",
        views.guest_info_list,
        name="guest_info_list",
    ),
    path(
        "guest-info-create/",
        views.guest_info_create,
        name="guest_info_create",
    ),
    path(
        "<int:guest_info_id>/guest-info-edit/",
        views.guest_info_edit,
        name="guest_info_edit",
    ),
    path(
        "<int:guest_info_id>/guest-info-image-upload/",
        views.guest_info_image_upload,
        name="guest_info_image_upload",
    ),
    path(
        "<int:guest_info_id>/guest-info-delete/",
        views.guest_info_delete,
        name="guest_info_delete",
    ),
    path(
        "calendar",
        views.calendar,
        name="calendar",
    ),
    path(
        "terms_and_conditions/",
        views.terms_and_conditions,
        name="terms_and_conditions",
    ),
]
