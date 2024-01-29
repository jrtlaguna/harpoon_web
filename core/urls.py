from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("login", views.login_page, name="login"),
    path("features/", views.features_page, name="features"),
    path("about/", views.about_page, name="about"),
    path("contact_us/", views.contact_us_page, name="contact_us"),
    path(
        "document_download/<int:document_id>/",
        views.download_file,
        name="download_document",
    ),
    path(
        "remove_document/<int:document_id>/",
        views.remove_document,
        name="remove_document",
    ),
]
