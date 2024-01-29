from django.urls import path

from vessels import views

app_name = "vessels"

urlpatterns = [
    path("", views.vessel_dashboard, name="dashboard"),
    path("<int:pk>/", views.vessel_profile, name="profile_view"),
    path("<int:pk>/edit/", views.vessel_profile_edit, name="profile_edit"),
    path("vessel-setup/", views.new_vessel, name="vessel_setup"),
    path("vessel-setup/<int:pk>/", views.new_vessel, name="vessel_setup"),
    path(
        "document-upload/<int:vessel_id>/",
        views.upload_vessel_documents,
        name="documents_upload",
    ),
]
