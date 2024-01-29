import pytest

from django.contrib.auth import authenticate
from django.core import mail

from authentication.models import User, PasswordResetCode
from authentication.services import send_password_reset_code, change_user_password


@pytest.mark.django_db
def test_can_send_password_reset_code():
    admin = User.objects.create(email="admin@example.com")
    code_has_been_sent = send_password_reset_code(email=admin.email)

    code = PasswordResetCode.objects.get(user=admin)
    assert str(code) in mail.outbox[0].body
    assert code_has_been_sent


@pytest.mark.django_db
def test_will_not_send_a_code_to_unused_emails():
    unused_email = "unused_email@example.com"
    code_has_been_sent = send_password_reset_code(email=unused_email)

    assert code_has_been_sent is False
    assert bool(PasswordResetCode.objects.filter(user__email=unused_email)) is False


@pytest.mark.django_db
def test_can_change_a_users_password():
    admin = User.objects.create(email="test@example.com")
    new_password = "p@ssword!"
    change_user_password(email=admin.email, password=new_password)

    assert bool(authenticate(email=admin.email, password=new_password))
