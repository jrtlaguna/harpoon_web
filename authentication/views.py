from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from authentication.models import User


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Redirects the user to their appropriate dashboard.
    """
    user: User = request.user
    if user.is_admin:
        return redirect(reverse("admins:dashboard"))

    if user.is_guest:
        return redirect(reverse("guests:dashboard"))


def handler404(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    """
    404 redirect handler
    """
    user: User = request.user
    if not user.is_authenticated:
        return redirect(reverse("core:home_page"))

    if user.role == "ADMIN":
        return redirect(reverse("admins:dashboard"))

    return redirect(reverse("guests:dashboard"))
