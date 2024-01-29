from django.contrib import admin

from vessels.models import Vessel


@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "charter_type",
        "admin",
        "imo_number",
        "is_active",
    ]
    search_fields = [
        "name",
        "admin",
        "imo_number",
        "is_active",
    ]
    list_filter = [
        "charter_type",
    ]
    autocomplete_fields = [
        "admin",
    ]
