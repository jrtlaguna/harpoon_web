from django.contrib import admin

from charter.models import (
    GuestDetail,
    Charter,
    FoodPreferences,
    MealAndRoomPreferences,
    BreakfastSelection,
    LunchSelection,
    DinnerSelection,
    DietServicesSizesPreferences,
    OtherServices,
    BeveragesAndAlcoholicPreferences,
    MilkSelection,
    CoffeeSelection,
    TeaSelection,
    WaterSelection,
    JuiceSelection,
    SodasAndMixersSelection,
    AddOnsSelection,
)


@admin.register(GuestDetail)
class GuestDetailAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name", "nationality"]
    search_fields = ["first_name", "last_name", "email", "nationality"]


@admin.register(Charter)
class CharterAdmin(admin.ModelAdmin):
    list_display = [
        "vessel",
        "principal_guest",
        "created_by",
        "apa_budget",
        "is_complete",
    ]
    search_fields = [
        "principal_guest__email",
        "principal_guest__first_name",
        "principal_guest__last_name",
        "vessel__name",
    ]
    list_filter = ["is_complete"]


@admin.register(FoodPreferences)
class FoodPreferencesAdmin(admin.ModelAdmin):
    list_display = ["guest", "is_complete"]
    search_fields = [
        "guest__first_name",
        "guest__last_name",
    ]

    def is_complete(self, obj):
        return obj.is_complete

    is_complete.boolean = True
    is_complete.short_description = "Is Complete"


@admin.register(MealAndRoomPreferences)
class MealAndRoomPreferencesAdmin(admin.ModelAdmin):
    list_display = ["guest", "created_at", "updated_at"]
    search_fields = ["guest__first_name", "guest__last_name", "guest__email"]


@admin.register(BreakfastSelection)
class BreakfastSelectionAdmin(admin.ModelAdmin):
    list_display = ["meal_and_room_preference"]
    search_fields = [
        "meal_and_room_preference__guest__first_name",
        "meal_and_room_preference__guest__last_name",
        "meal_and_room_preference__guest__email",
    ]


@admin.register(LunchSelection)
class LunchSelectionAdmin(admin.ModelAdmin):
    list_display = ["meal_and_room_preference"]
    search_fields = [
        "meal_and_room_preference__guest__first_name",
        "meal_and_room_preference__guest__last_name",
        "meal_and_room_preference__guest__email",
    ]


@admin.register(DinnerSelection)
class DinnerSelectionAdmin(admin.ModelAdmin):
    list_display = ["meal_and_room_preference"]
    search_fields = [
        "meal_and_room_preference__guest__first_name",
        "meal_and_room_preference__guest__last_name",
        "meal_and_room_preference__guest__email",
    ]


@admin.register(DietServicesSizesPreferences)
class DietServicesSizesPreferencesAdmin(admin.ModelAdmin):
    list_display = ["guest", "created_at", "updated_at"]
    search_fields = ["guest__first_name", "guest__last_name", "guest__email"]


@admin.register(OtherServices)
class OtherServicesAdmin(admin.ModelAdmin):
    list_display = ["diet_services_sizes_preferences"]
    search_fields = [
        "diet_services_sizes_preferences__guest__first_name",
        "diet_services_sizes_preferences__guest__last_name",
        "diet_services_sizes_preferences__guest__email",
    ]


@admin.register(BeveragesAndAlcoholicPreferences)
class BeveragesAndAlcoholicPreferencesAdmin(admin.ModelAdmin):
    list_display = ["guest", "created_at", "updated_at"]
    search_fields = ["guest__first_name", "guest__last_name", "guest__email"]


@admin.register(MilkSelection)
class MilkSelectionAdmin(admin.ModelAdmin):
    list_display = ["beverages_and_alcoholic_preferences"]
    search_fields = [
        "beverages_and_alcoholic_preferences__guest__first_name",
        "beverages_and_alcoholic_preferences__guest__last_name",
        "beverages_and_alcoholic_preferences__guest__email",
    ]


@admin.register(CoffeeSelection)
class CoffeeSelectionAdmin(admin.ModelAdmin):
    list_display = ["beverages_and_alcoholic_preferences"]
    search_fields = [
        "beverages_and_alcoholic_preferences__guest__first_name",
        "beverages_and_alcoholic_preferences__guest__last_name",
        "beverages_and_alcoholic_preferences__guest__email",
    ]


@admin.register(TeaSelection)
class TeaSelectionAdmin(admin.ModelAdmin):
    list_display = ["beverages_and_alcoholic_preferences"]
    search_fields = [
        "beverages_and_alcoholic_preferences__guest__first_name",
        "beverages_and_alcoholic_preferences__guest__last_name",
        "beverages_and_alcoholic_preferences__guest__email",
    ]


@admin.register(WaterSelection)
class WaterSelectionAdmin(admin.ModelAdmin):
    list_display = ["beverages_and_alcoholic_preferences"]
    search_fields = [
        "beverages_and_alcoholic_preferences__guest__first_name",
        "beverages_and_alcoholic_preferences__guest__last_name",
        "beverages_and_alcoholic_preferences__guest__email",
    ]


@admin.register(JuiceSelection)
class JuiceSelectionAdmin(admin.ModelAdmin):
    list_display = ["beverages_and_alcoholic_preferences"]
    search_fields = [
        "beverages_and_alcoholic_preferences__guest__first_name",
        "beverages_and_alcoholic_preferences__guest__last_name",
        "beverages_and_alcoholic_preferences__guest__email",
    ]


@admin.register(SodasAndMixersSelection)
class SodasAndMixersSelectionAdmin(admin.ModelAdmin):
    list_display = ["beverages_and_alcoholic_preferences"]
    search_fields = [
        "beverages_and_alcoholic_preferences__guest__first_name",
        "beverages_and_alcoholic_preferences__guest__last_name",
        "beverages_and_alcoholic_preferences__guest__email",
    ]


@admin.register(AddOnsSelection)
class AddOnsSelectionAdmin(admin.ModelAdmin):
    list_display = ["beverages_and_alcoholic_preferences"]
    search_fields = [
        "beverages_and_alcoholic_preferences__guest__first_name",
        "beverages_and_alcoholic_preferences__guest__last_name",
        "beverages_and_alcoholic_preferences__guest__email",
    ]
