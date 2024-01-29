from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def anonymous_required(view_func):
    """
    Only allow anonymous (non-authenticated) users to access a specific view.
    """

    def wrap(request, *args, **kwargs):
        if not request.user.is_anonymous:
            return redirect(reverse("authentication:dashboard"))
        return view_func(request, *args, **kwargs)

    return wrap


def guest_required(view_func):
    """
    Only allow users marked as guests to access a specific view.
    """

    def wrap(request, *args, **kwargs):
        if not request.user.is_guest:
            messages.error(
                request,
                "You need to be a guest to perform this action.",
                fail_silently=True,
            )
            if referer := request.META.get("HTTP_REFERER"):
                return redirect(referer)
            else:
                logout(request)
                return redirect("core:home_page")
        return view_func(request, *args, **kwargs)

    return wrap


def admin_required(view_func):
    """
    Only allow users marked as admins to access a specific view.
    """

    def wrap(request, *args, **kwargs):
        if not (request.user.is_admin and hasattr(request.user, "admin_profile")):
            messages.error(
                request,
                "You need to be an admin to perform this action.",
                fail_silently=True,
            )
            if referer := request.META.get("HTTP_REFERER"):
                return redirect(referer)
            else:
                logout(request)
                return redirect("core:home_page")
        return view_func(request, *args, **kwargs)

    return wrap
