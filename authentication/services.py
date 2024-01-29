from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from authentication.models import User, PasswordResetCode


def send_password_reset_code(*, email: str) -> bool:
    """
    Sends a password reset code to the given email.
    Returns whether the email has been sent or not.
    """

    try:
        user = User.objects.get(email=email)
        code = PasswordResetCode.objects.create(user=user)
        message = render_to_string(
            "authentication/email/password_reset_code.html", {"code": code}
        )
        send_mail(
            "Password Reset Code",
            message,
            settings.EMAIL_FROM,
            [email],
            html_message=message,
        )
        return True
    except User.DoesNotExist:
        return False


def change_user_password(*, email: str, password: str) -> User:
    """
    Changes the user that owns the given email to the provided password.
    Returns the updated user instance,
    """
    user = User.objects.get(email=email)
    user.set_password(password)
    user.save()

    return User
