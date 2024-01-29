from django.contrib import admin

from admins.models import AdminProfile, CrewProfile


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role"]
    search_fields = ["user__first_name", "user__last_name", "user__email"]
    list_filter = ["role"]


class AdminProfileInline(admin.StackedInline):
    model = AdminProfile


class AdminAdmin(admin.ModelAdmin):
    inlines = (AdminProfileInline,)


admin.site.register(CrewProfile)
