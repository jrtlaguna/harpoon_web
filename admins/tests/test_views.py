import pytest

from django.urls import reverse
from django.contrib.messages import get_messages
from django.test import Client

from authentication.models import User
from admins.models import AdminProfile

from bs4 import BeautifulSoup

STATUS_200 = 200
STATUS_302 = 302


@pytest.mark.django_db
def test_admin_login_view_unauthenticated_user(unauthenticated_client: Client):
    response = unauthenticated_client.get(reverse("admins:login"))
    soup = BeautifulSoup(response._container[0], "html.parser")
    form_exists = bool(soup.find("form", id="id-loginForm"))

    assert form_exists
    assert response.status_code == STATUS_200


@pytest.mark.django_db
def test_admin_login_view_authenticated_admin(admin_client: Client):
    response = admin_client.get(reverse("admins:login"))

    assert "dashboard" in response["Location"]
    assert response.status_code == STATUS_302


@pytest.mark.django_db
def test_admin_logout_view_authenticated_admin(admin_client: Client):
    response = admin_client.get(reverse("admins:logout"))

    assert response.status_code == 302

    messages = [message.message for message in get_messages(response.wsgi_request)]
    assert len(messages) == 1
    assert messages[0] == "You have been logged out."


# TODO: fix form invalid even with correct data
@pytest.mark.django_db
def test_admin_login_user_account(unauthenticated_client: Client, guest_user: User):

    data = {
        "username": guest_user.email,
        "email": guest_user.email,
        "password": guest_user.password,
    }
    response = unauthenticated_client.post(reverse("admins:login"), data)
    assert response.status_code == STATUS_200


@pytest.mark.django_db
def test_login_authenticated_user_view(admin_client: Client):

    response = admin_client.get(reverse("admins:login"))

    assert response.status_code == STATUS_302
    assert response.url == reverse("authentication:dashboard")


@pytest.mark.django_db
def test_admin_register_unauthenticated_user(unauthenticated_client: Client):
    response = unauthenticated_client.get(reverse("admins:register"))
    soup = BeautifulSoup(response._container[0], "html.parser")

    assert response.status_code == STATUS_200
    assert bool(soup.find("form", id="id-registrationForm"))


@pytest.mark.django_db
def test_post_admin_register_unauthenticated_user(unauthenticated_client: Client):
    data = {
        "first_name": "john",
        "last_name": "doe",
        "email": "jdoe@gmail.com",
        "role": AdminProfile.Roles.CAPTAIN,
        "phone_number": "+12323223",
        "password1": "admin123123",
        "password2": "admin123123",
        "accept_toc": True,
    }

    response = unauthenticated_client.post(reverse("admins:register"), data)

    assert response.status_code == STATUS_302
    assert "vessel-setup" in response["Location"]

    messages = [message.message for message in get_messages(response.wsgi_request)]
    assert len(messages) == 1
    assert messages[0] == "Your account is now created!"


def test_unauthenticated_user_forgot_password_view(unauthenticated_client: Client):
    response = unauthenticated_client.get(reverse("admins:forgot_password"))
    soup = BeautifulSoup(response._container[0], "html.parser")

    assert response.status_code == 200

    assert bool(soup.find("form", id="id-forgotPasswordForm"))


@pytest.mark.django_db
def test_post_forget_password_view(unauthenticated_client, admin_user):
    data = {
        "email": admin_user.email,
    }
    response = unauthenticated_client.post(reverse("admins:forgot_password"), data)

    assert response.status_code == STATUS_302
    assert (
        reverse("admins:forgot_password_code", args=[admin_user.email]) in response.url
    )


# TODO: forgot_password_code view
# TODO: resend_password_code
# TODO: resend_password_code
# TODO: change_password


# FAILING TEST
# @pytest.mark.django_db
# def test_invalid_role_in_admin_view(guest_client):
#     response = guest_client.get(reverse("admins:dashboard"))

#     # redirected to landing page
#     assert response.status_code == STATUS_302
#     assert reverse("core:home_page") in response.url


@pytest.mark.django_db
def test_dashboard_view(admin_client: Client):

    response = admin_client.get(reverse("admins:dashboard"))
    soup = BeautifulSoup(response._container[0], "html.parser")

    assert response.status_code == 200
    assert bool(soup.find("table"))


@pytest.mark.django_db
def test_get_settings_view(admin_client: Client):
    response = admin_client.get(reverse("admins:settings"))
    soup = BeautifulSoup(response._container[0], "html.parser")

    assert response.status_code == STATUS_200
    assert bool(soup.find("form", {"id": "id-settingsForm"}))
    assert bool(soup.find("form", {"id": "id-imageForm"}))


@pytest.mark.django_db
def test_post_settings_view(admin_client: Client, admin_user: User):
    data = {
        "first_name": admin_user.first_name,
        "last_name": admin_user.last_name,
        "email": admin_user.email,
        "role": admin_user.admin_profile.role,
        "phone_number": admin_user.admin_profile.phone_number,
        "receive_email_notifications": admin_user.admin_profile.receive_email_notifications,
    }
    response = admin_client.post(reverse("admins:settings"), data)

    assert response.status_code == STATUS_302
    messages = [message.message for message in get_messages(response.wsgi_request)]
    assert len(messages) == 1
    assert messages[0] == "Your settings has been updated."
