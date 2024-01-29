from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse

from bs4 import BeautifulSoup

from authentication.models import User
from charter.factories import GuestFactory
from charter.models import GuestDetail
from guests import views
from guests.factories import GuestProfileFactory


class GuestViewsTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.details = GuestFactory(email="guest@dwm.com")
        self.user = User.objects.create(
            email="guest@dwm.com", role=User.Roles.GUEST, password="1"
        )
        self.guest_profile = GuestProfileFactory(user=self.user)
        self.guest_profile.details = GuestDetail.objects.create(
            profile=self.guest_profile,
            email="guest@dwm.com",
        )

    def test_unauthenticated_user_guest_views(self):
        request = self.factory.get(reverse("guests:dashboard"))
        request.user = AnonymousUser()

        response = views.dashboard(request)

        self.assertEquals(response.status_code, 302)

    # def test_authenticated_user_guest_views(self):
    #     request = self.factory
    #     request.user = self.user

    #     response = views.dashboard(request)

    #     self.assertEquals(response.status_code, 200)

    # def test_user_without_profile(self):
    #     request = self.factory
    #     request.user = User.objects.create(
    #         email="guest2@dwm.com", role=User.Roles.GUEST, password="1"
    #     )

    #     response = views.dashboard(request)

    #     self.assertEquals(response.status_code, 400)
