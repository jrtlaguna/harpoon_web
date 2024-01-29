import json

from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse

from authentication.decorators import admin_required
from authentication.models import User
from admins.models import AdminProfile
from admins.utils import get_admin_notifications
from core.models import Document
from vessels.forms import VesselForm, VesselDocumentForm, VesselProfileForm
from vessels.models import Vessel
from vessels.services import create_vessel, update_vessel


@login_required
@admin_required
def new_vessel(request: HttpRequest, pk: int = None) -> HttpResponse:
    """
    Creating a new Vessel or welcome page for new Admin
    """
    user: User = request.user
    ctx = {}
    vessel: Vessel = None
    if pk:
        vessel: Vessel = get_object_or_404(Vessel, id=pk, admin=user.admin_profile)

    if request.method == "POST":
        form = VesselForm(data=request.POST, imo_number="")
        if form.is_valid():
            if not vessel:
                vessel = create_vessel(
                    admin=user.admin_profile,
                    name=form.cleaned_data.get("name").capitalize(),
                    imo_number=form.cleaned_data.get("imo_number"),
                    charter_type=form.cleaned_data.get("charter_type"),
                )
            else:
                vessel = update_vessel(
                    vessel=vessel,
                    **form.cleaned_data,
                )
            ctx["vessel"] = vessel
            return JsonResponse({"message": "Successfully created vessel."})
    else:
        form = VesselForm(imo_number="")
        if vessel:
            form = VesselForm(
                initial={
                    "name": vessel.name,
                    "charter_type": vessel.charter_type,
                },
                imo_number=vessel.imo_number,
            )
    ctx["form"] = form
    return render(request, "vessels/vessel_details.html", ctx)


@login_required
@admin_required
def vessel_dashboard(request: HttpRequest) -> HttpResponse:
    """
    Creating a new Vessel or welcome page for new Admin
    """
    user: User = request.user

    vessels = user.admin_profile.vessels.all().order_by("-is_active", "-created_at")

    notifications, new_notifications = get_admin_notifications(
        user.admin_profile,
    )
    ctx = {
        "vessels": vessels,
        "notifications": notifications,
        "new_notifications": new_notifications,
    }
    return render(request, "vessels/vessel_dashboard.html", ctx)


@login_required
@admin_required
def vessel_profile(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Viewing Vessel details
    """
    admin_profile: AdminProfile = request.user.admin_profile
    notifications, new_notifications = get_admin_notifications(
        admin_profile,
    )
    ctx: dict = {
        "notifications": notifications,
        "new_notifications": new_notifications,
    }

    vessel = get_object_or_404(Vessel, id=pk, admin=admin_profile)
    document_form = VesselDocumentForm(vessel_id=vessel.id)
    ctx["document_form"] = document_form

    if vessel is None:
        ctx["vessels"] = admin_profile.vessels.all().order_by(
            "is_active", "-created_at"
        )
        return render(request, "vessels/vessel_dashboard.html", ctx)

    ctx["vessel"] = vessel
    ctx["has_upcoming"] = vessel.charters.exists()
    return render(request, "vessels/vessel_profile.html", ctx)


@login_required
@admin_required
def vessel_profile_edit(request: HttpRequest, pk: int) -> HttpResponse:
    vessel: Vessel = get_object_or_404(Vessel, id=pk)
    if not vessel:
        return HttpResponseRedirect(reverse("vessels:dashboard"))
    notifications, new_notifications = get_admin_notifications(
        request.user.admin_profile,
    )
    document_form = VesselDocumentForm(vessel_id=pk)
    ctx = {
        "vessel": vessel,
        "notifications": notifications,
        "document_form": document_form,
        "new_notifications": new_notifications,
    }
    if request.method == "POST":
        form = VesselForm(data=request.POST, imo_number=vessel.imo_number)
        if form.is_valid():
            vessel = update_vessel(
                vessel=vessel,
                **form.cleaned_data,
            )
            ctx["vessel"] = vessel
            return HttpResponse(
                json.dumps({"nothing to see": "this isn't happening"}),
                content_type="application/json",
            )
    else:
        ctx["form"] = VesselProfileForm(
            initial={
                "name": vessel.name,
                "charter_type": vessel.charter_type,
                "imo_number": vessel.imo_number or "",
            },
            imo_number=vessel.imo_number or "",
        )

        return render(request, "vessels/vessel_profile.html", ctx)


def upload_vessel_documents(request: HttpRequest, vessel_id: int) -> HttpResponse:
    user: User = request.user
    document_form = VesselDocumentForm(request.POST, request.FILES, vessel_id=vessel_id)
    document_list = []
    if document_form.is_valid():
        for f in request.FILES.getlist("document"):
            document_list.append(
                Document(
                    model_id=vessel_id,
                    model=Document.ModelChoices.VESSEL,
                    uploaded_by=user,
                    document=f,
                )
            )
    if document_list:
        Document.objects.bulk_create(document_list)
    return HttpResponseRedirect(reverse("vessels:profile_view", args=[vessel_id]))
