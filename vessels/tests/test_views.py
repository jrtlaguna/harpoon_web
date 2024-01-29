from bs4 import BeautifulSoup
import pytest

from django.urls import reverse
from django.contrib.messages import get_messages
from django.http import HttpResponse, HttpResponseRedirect
from django.test import Client

from authentication.models import User
from vessels.models import Vessel


@pytest.mark.django_db
def test_get_new_vessel_view_unauthenticated_user(unauthenticated_client: Client):
    response = unauthenticated_client.get(reverse("vessels:vessel_setup"))

    assert response.status_code == 302


@pytest.mark.django_db
def test_get_new_vessel_view(admin_client: Client):
    response: HttpResponse = admin_client.get(reverse("vessels:vessel_setup"))

    soup = BeautifulSoup(response._container[0], "html.parser")

    assert bool(soup.find("form", {"id": "id-vesselForm"}))
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_post_new_vessel(admin_client: Client):
#     data = {
#         "name": "Test Vessel",
#         "charter_type": Vessel.CharterType.MOTOR_YACHT,
#         "imo_number": "123123",
#     }
#     response: HttpResponse = admin_client.post(reverse("vessels:vessel_setup"), data)
#     latest_vessel = Vessel.objects.last()

#     assert response.url in reverse("vessels:preference_sheet", args=[latest_vessel.id])
#     assert response.status_code == 302
#     assert latest_vessel.name == data.get("name").capitalize()
#     assert latest_vessel.charter_type == data.get("charter_type")
#     assert latest_vessel.imo_number == data.get("imo_number")


@pytest.mark.django_db
def test_get_existing_vessel_new_vessel_view(admin_client: Client, admin_user: User):
    vessel: Vessel = admin_user.admin_profile.vessels.last()
    response: HttpResponse = admin_client.get(
        reverse("vessels:vessel_setup", args=[vessel.id])
    )
    soup = BeautifulSoup(response._container[0], "html.parser")
    name_field = soup.find("input", {"name": "name"})
    imo_number_field = soup.find("input", {"name": "imo_number"})

    assert bool(soup.find("form", {"id": "id-vesselForm"}))
    assert response.status_code == 200
    assert name_field.get("value") == vessel.name
    assert imo_number_field.get("value") == vessel.imo_number


@pytest.mark.django_db
def test_get_vessel_setup_sheet_invalid_pk(admin_client: Client):
    response: HttpResponse = admin_client.get(
        reverse("vessels:vessel_setup", args=[100])
    )

    assert response.status_code == 404


# @pytest.mark.django_db
# def test_get_vessel_preference_sheet(admin_client: Client, admin_user: User):
#     vessel: Vessel = admin_user.admin_profile.vessels.last()
#     response: HttpResponse = admin_client.get(
#         reverse("vessels:preference_sheet", args=[vessel.id])
#     )

#     assert response.status_code == 200


# @pytest.mark.django_db
# def test_get_vessel_preference_sheet_invalid_pk(admin_client: Client):
#     response: HttpResponse = admin_client.get(
#         reverse("vessels:preference_sheet", args=[100])
#     )

#     assert response.status_code == 404


@pytest.mark.django_db
def test_get_vessel_summary(admin_client: Client, admin_user: User):
    vessel: Vessel = admin_user.admin_profile.vessels.last()
    response: HttpResponse = admin_client.get(
        reverse("vessels:summary", args=[vessel.id])
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_get_vessel_summary_invalid_pk(admin_client: Client):
    response: HttpResponse = admin_client.get(reverse("vessels:summary", args=[100]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_vessel_dashboard(admin_client: Client, admin_user: User):
    active_vessel = admin_user.admin_profile.vessels.filter(is_active=True).count()
    response: HttpResponse = admin_client.get(reverse("vessels:dashboard"))
    soup = BeautifulSoup(response._container[0], "html.parser")
    response_active_vessels = len(
        soup.find("span", {"class": "badge badge-pill badge-success px-3"})
    )

    assert response.status_code == 200
    assert response_active_vessels == active_vessel


@pytest.mark.django_db
def test_get_vessel_profile(admin_client: Client, admin_user: User):
    vessel: Vessel = admin_user.admin_profile.vessels.last()
    response = admin_client.get(reverse("vessels:profile_view", args=[vessel.id]))
    soup = BeautifulSoup(response._container[0], "html.parser")

    title = soup.find("h5").string
    assert vessel.name in title
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_not_existing_vessel_profile(admin_client: Client):
    response: HttpResponse = admin_client.get(
        reverse("vessels:profile_view", args=[100])
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_get_profile_edit(admin_client: Client, admin_user: User):
    vessel: Vessel = admin_user.admin_profile.vessels.last()
    response = admin_client.get(reverse("vessels:profile_edit", args=[vessel.id]))

    assert response.status_code == 200


# TODO: add update vessel test
# @pytest.mark.django_db
# def test_post_profile_edit(admin_client: Client, admin_user: User):
#     vessel: Vessel = admin_user.admin_profile.vessels.last()
#     data = {
#         "name": "New Vessel Name",
#     }
#     response: HttpResponse = admin_client.get(
#         reverse("vessels:profile_edit", args=[vessel.id])
#     )
#     import pdb

#     pdb.set_trace()


@pytest.mark.django_db
def test_get_profile_edit_invalid_pk(admin_client: Client):
    response = admin_client.get(reverse("vessels:profile_edit", args=[100]))

    assert response.status_code == 404
