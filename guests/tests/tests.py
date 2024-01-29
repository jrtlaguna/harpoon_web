from django.test import TestCase

from guests.services import create_guest_account


class GuestServicesTest(TestCase):
    def test_can_create_new_guest_accounts(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "jdoe@example.com",
            "phone_number": "+123456789",
            "password": "p@ssword!",
        }

        guest = create_guest_account(**data)

        self.assertEqual(guest.first_name, data["first_name"])
        self.assertEqual(guest.last_name, data["last_name"])
        self.assertEqual(guest.email, data["email"])

        # An guestProfile instance will be created as well.
        self.assertEqual(guest.guest_profile.phone_number, data["phone_number"])
