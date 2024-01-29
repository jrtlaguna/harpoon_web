# import factory

# from charter.factories import GuestFactory
# from charter.models import (
#     BeveragesAndAlcoholicPreferences,
#     FoodPreferences,
#     MealAndRoomPreferences,
#     DietServicesSizesPreferences,
#     # SELECTION_MODELS
#     BreakfastSelection,
#     LunchSelection,
#     DinnerSelection,
#     OtherServices,
#     MilkSelection,
#     CoffeeSelection,
#     TeaSelection,
#     WaterSelection,
#     JuiceSelection,
#     SodasAndMixersSelection,
#     AddOnsSelection,
# )


# class FoodPreferencesFactory(factory.django.DjangoModelFactory):
#     guest = factory.SubFactory(GuestFactory)
#     general_cuisine = FoodPreferences.GeneralCuisine.THAI
#     general_cuisine_notes = "Note GC"
#     fish_and_shellfish = FoodPreferences.FishAndShellfish.TROUT
#     fish_and_shellfish_notes = "Note FS"
#     meat = FoodPreferences.Meat.VEAL
#     meat_notes = "Note MT"
#     bread = FoodPreferences.Bread.WHITE
#     bread_notes = "Note BRD"
#     salad = FoodPreferences.Salad.SEAFOOD
#     salad_notes = "Note SLD"
#     soup = FoodPreferences.Soup.VICHYSSOISE
#     soup_notes = "Note SOP"
#     cheese = FoodPreferences.Cheese.PARMESAN
#     cheese_notes = "Note CHS"
#     dessert = FoodPreferences.Dessert.TARTS
#     dessert_notes = "Note DSRT"

#     class Meta:
#         model = FoodPreferences


# class MealAndRoomPreferencesFactory(factory.django.DjangoModelFactory):
#     guest = factory.SubFactory(GuestFactory)
#     breakfast_time = MealAndRoomPreferences.time_choices[0]
#     breakfast_note = "Note Breakfast"
#     lunch_time = MealAndRoomPreferences.time_choices[12]
#     lunch_note = "Note Lunch"
#     dinner_time = MealAndRoomPreferences.time_choices[24]
#     dinner_note = "Note Dinner"
#     canapes_time = MealAndRoomPreferences.CanapesTime.BEFORE_LUNCH
#     canapes_selection = MealAndRoomPreferences.CanapesTypes.LIGHT
#     midmorning_snacks = MealAndRoomPreferences.MidMorningSnacks.SWEET
#     midafternoon_snacks = MealAndRoomPreferences.MidAfternoonSnacks.SAVORY
#     favorite_flowers = "Sunflower"

#     class Meta:
#         model = MealAndRoomPreferences


# class DietServicesSizesPreferencesFactory(factory.django.DjangoModelFactory):
#     guest = factory.SubFactory(GuestFactory)
#     dietary_restrictions = DietServicesSizesPreferences.DietaryRestrictions.PESCATARIAN
#     dietary_restrictions_other_notes = ""
#     dietary_restrictions_notes = "Note"
#     preferred_room_temperature = "18° C"
#     other_services_other_notes = "Note Other Services"
#     shirt_sizing = DietServicesSizesPreferences.ShirtSizing.WOMENS
#     international_shirt_sizing = (
#         DietServicesSizesPreferences.InternationalShirtSizing.UK
#     )
#     shirt_size = DietServicesSizesPreferences.ShirtSizes.XL
#     shoe_sizing = DietServicesSizesPreferences.ShoeSizing.WOMENS
#     international_shoe_sizing = DietServicesSizesPreferences.InternationalShoeSizing.UK
#     shoe_size = 9

#     class Meta:
#         model = DietServicesSizesPreferences


# class BeveragesAndAlcoholicPreferencesFactory(factory.django.DjangoModelFactory):
#     guest = factory.SubFactory(GuestFactory)
#     milk_note = "milk note"
#     coffee_note = "coffe note"
#     tea_note = "tea note"
#     water_note = "water note"
#     juice_note = "juice note"
#     sodas_and_mixers_note = "sodas and mixers note"
#     add_ons_note = "ad ons note"
#     whiskey_name = "Whiskey Brand"
#     whiskey_quantity = 10
#     brandy_name = "Brandy Brand"
#     brandy_quantity = 10
#     vodka_name = "Vodka Brand"
#     vodka_quantity = 10
#     tequila_name = "Tequila Brand"
#     tequila_quantity = 10
#     rum_name = "Rum Brand"
#     rum_quantity = 10
#     liquors_name = "Liquor Brand"
#     liquors_quantity = 10
#     cocktail_name = "Cocktail Brand"
#     cocktail_quantity = 10
#     port_beer_name = "Port/Beer Brand"
#     port_beer_quantity = 10
#     red_wine_name = "Red Wine Brand"
#     red_wine_quantity = 10
#     white_wine_name = "White Wine Brand"
#     white_wine_quantity = 10
#     champagne_name = "Champagne Brand"
#     champagne_quantity = 10
#     other_name = "Other Alcohol"
#     other_quantity = 10

#     class Meta:
#         model = BeveragesAndAlcoholicPreferences


# class BreakfastSelectionFactory(factory.django.DjangoModelFactory):
#     name = BreakfastSelection.BreakfastSelection.BUFFET

#     class Meta:
#         model = BreakfastSelection


# class LunchSelectionFactory(factory.django.DjangoModelFactory):
#     name = LunchSelection.LunchSelection._4_COURSE

#     class Meta:
#         model = LunchSelection


# class DinnerSelectionFactory(factory.django.DjangoModelFactory):
#     name = DinnerSelection.DinnerSelection.RUSSIAN_STYLE

#     class Meta:
#         model = DinnerSelection


# class OtherServicesFactory(factory.django.DjangoModelFactory):
#     name = DietServicesSizesPreferences.OtherServices.DIVING_EXCURSION

#     class Meta:
#         model = OtherServices


# class MilkSelectionFactory(factory.django.DjangoModelFactory):
#     name = BeveragesAndAlcoholicPreferences.MilkSelections.WHOLE

#     class Meta:
#         model = MilkSelection


# class CoffeeSelectionFactory(factory.django.DjangoModelFactory):
#     name = BeveragesAndAlcoholicPreferences.CoffeeSelections.AMERICAN

#     class Meta:
#         model = CoffeeSelection


# class TeaSelectionFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = TeaSelection


# class WaterSelectionFactory(factory.django.DjangoModelFactory):
#     name = BeveragesAndAlcoholicPreferences.WaterSelections.SPARKLING

#     class Meta:
#         model = WaterSelection


# class JuiceSelectionFactory(factory.django.DjangoModelFactory):
#     name = BeveragesAndAlcoholicPreferences.JuiceSelections.GRAPE_FRUIT

#     class Meta:
#         model = JuiceSelection


# class SodasAndMixersSelectionFactory(factory.django.DjangoModelFactory):
#     name = BeveragesAndAlcoholicPreferences.SodasMixersSelections._7_UP

#     class Meta:
#         model = SodasAndMixersSelection


# class AddOnsSelectionFactory(factory.django.DjangoModelFactory):
#     name = BeveragesAndAlcoholicPreferences.AddOnsSelections.SUGAR

#     class Meta:
#         model = AddOnsSelection
