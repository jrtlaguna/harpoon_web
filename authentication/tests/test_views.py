import pytest

from django.urls import reverse
from django.test.testcases import SimpleTestCase

REDIRECT_STATUS_CODE = 302


@pytest.mark.django_db
def test_dashboard_redirect_unauthenticated_user(unauthenticated_client):
    response = unauthenticated_client.get(reverse("authentication:dashboard"))

    assert reverse("core:home_page") in response.url
    assert response.status_code == REDIRECT_STATUS_CODE


@pytest.mark.django_db
def test_dashboard_redirect_guest_user(guest_client):
    response = guest_client.get(reverse("authentication:dashboard"))

    assert reverse("guests:dashboard") in response.url
    assert response.status_code == REDIRECT_STATUS_CODE


@pytest.mark.django_db
def test_dashboard_redirect_admin_user(admin_client):
    response = admin_client.get(reverse("authentication:dashboard"))

    assert reverse("admins:dashboard") in response.url
    assert response.status_code == REDIRECT_STATUS_CODE
