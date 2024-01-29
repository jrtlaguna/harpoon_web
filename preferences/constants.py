from charter.models import (
    BeveragesAndAlcoholicPreferences,
    BreakfastSelection,
    DinnerSelection,
    FoodPreferences,
    LunchSelection,
    MealAndRoomPreferences,
    DietServicesSizesPreferences,
)

GENERAL_CUISINE = FoodPreferences.GeneralCuisine.choices
FISH_SHELLFISH = FoodPreferences.FishAndShellfish.choices
MEAT = FoodPreferences.Meat.choices
BREAD = FoodPreferences.Bread.choices
SOUP = FoodPreferences.Soup.choices
SALAD = FoodPreferences.Salad.choices
CHEESE = FoodPreferences.Cheese.choices
DESSERT = FoodPreferences.Dessert.choices

CANAPES_TIME_CHOICES = MealAndRoomPreferences.CanapesTime.choices
CANAPES_TYPES = MealAndRoomPreferences.CanapesTypes.choices
MID_MORNING_SNACKS = MealAndRoomPreferences.MidMorningSnacks.choices
MID_AFTERNOON_SNACKS = MealAndRoomPreferences.MidAfternoonSnacks.choices

BREAKFAST = BreakfastSelection.BreakfastSelection.choices
LUNCH = LunchSelection.LunchSelection.choices
DINNER = DinnerSelection.DinnerSelection.choices

DIETARY_RESTRICTIONS = MealAndRoomPreferences.DietaryRestrictions.choices + [
    ("OTHER", "Other")
]
OTHER_SERVICES = DietServicesSizesPreferences.OtherServices.choices + [
    ("OTHER", "Other")
]
SHIRT_SIZING = DietServicesSizesPreferences.ShirtSizing.choices
INTERNATIONAL_SHIRT_SIZING = (
    DietServicesSizesPreferences.InternationalShirtSizing.choices
)
SHIRT_SIZE = DietServicesSizesPreferences.ShirtSizes.choices
SHOE_SIZING = DietServicesSizesPreferences.ShoeSizing.choices
INTERNATIONAL_SHOE_SIZING = DietServicesSizesPreferences.InternationalShoeSizing.choices

MILK_SELECTIONS = BeveragesAndAlcoholicPreferences.MilkSelections.choices
COFFEE_SELECTIONS = BeveragesAndAlcoholicPreferences.CoffeeSelections.choices
TEA_SELECTIONS = BeveragesAndAlcoholicPreferences.TeaSelections.choices
WATER_SELECTIONS = BeveragesAndAlcoholicPreferences.WaterSelections.choices
JUICE_SELECTIONS = BeveragesAndAlcoholicPreferences.JuiceSelections.choices
SODAS_MIXERS_SELECTIONS = BeveragesAndAlcoholicPreferences.SodasMixersSelections.choices
ADD_ONS_SELECTIONS = BeveragesAndAlcoholicPreferences.AddOnsSelections.choices
