# from django.test import TestCase

# from charter.factories import GuestFactory
# from charter.models import (
#     BeveragesAndAlcoholicPreferences,
#     BreakfastSelection,
#     DietServicesSizesPreferences,
#     DinnerSelection,
#     FoodPreferences,
#     GuestDetail,
#     LunchSelection,
#     MealAndRoomPreferences,
# )
# from preferences.factories import (
#     BeveragesAndAlcoholicPreferencesFactory,
#     DietServicesSizesPreferencesFactory,
#     FoodPreferencesFactory,
#     MealAndRoomPreferencesFactory,
#     # SELECTIONS_FACTORIES
#     BreakfastSelectionFactory,
#     LunchSelectionFactory,
#     DinnerSelectionFactory,
#     OtherServicesFactory,
#     MilkSelectionFactory,
#     CoffeeSelectionFactory,
#     TeaSelectionFactory,
#     WaterSelectionFactory,
#     JuiceSelectionFactory,
#     SodasAndMixersSelectionFactory,
#     AddOnsSelectionFactory,
# )
# from preferences.models import KidsChoices
# from preferences.services import (
#     create_beverages_alcohol_preferences,
#     create_diet_services_sizes_preferences,
#     create_food_preferences,
#     create_meal_and_room_preferences,
#     update_beverages_alcohol_preferences,
#     update_diet_services_sizes_preferences,
#     update_food_preferences,
#     update_meal_and_room_preferences,
# )


# class PreferencesServicesTest(TestCase):
#     def test_can_create_food_preferences(self):
#         guest: GuestDetail = GuestFactory()

#         data = {
#             "guest": guest,
#             "general_cuisine": FoodPreferences.GeneralCuisine.AMERICAN,
#             "general_cuisine_notes": "Note GC",
#             "fish_and_shellfish": FoodPreferences.FishAndShellfish.CLAMS,
#             "fish_and_shellfish_notes": "Note FS",
#             "meat": FoodPreferences.Meat.BEEF,
#             "meat_notes": "Note MT",
#             "bread": FoodPreferences.Bread.BAGEL,
#             "bread_notes": "Note BRD",
#             "salad": FoodPreferences.Salad.BRIOCHE,
#             "salad_notes": "Note SLD",
#             "soup": FoodPreferences.Soup.BORSCHT,
#             "soup_notes": "Note SOP",
#             "cheese": FoodPreferences.Cheese.BLUE,
#             "cheese_notes": "Note CHS",
#             "dessert": FoodPreferences.Dessert.CAKE,
#             "dessert_notes": "Note DSRT",
#             "kids_meals": KidsChoices.CHICKEN,
#             "kids_meals_notes": "Note KDSMEALS",
#             "kids_allergies": "Allergies",
#         }

#         food_preferences = create_food_preferences(**data)

#         self.assertEqual(food_preferences.guest, data["guest"])
#         self.assertEqual(food_preferences.general_cuisine, data["general_cuisine"])
#         self.assertEqual(
#             food_preferences.general_cuisine_notes, data["general_cuisine_notes"]
#         )
#         self.assertEqual(
#             food_preferences.fish_and_shellfish, data["fish_and_shellfish"]
#         )
#         self.assertEqual(
#             food_preferences.fish_and_shellfish_notes, data["fish_and_shellfish_notes"]
#         )
#         self.assertEqual(food_preferences.meat, data["meat"])
#         self.assertEqual(food_preferences.meat_notes, data["meat_notes"])
#         self.assertEqual(food_preferences.bread, data["bread"])
#         self.assertEqual(food_preferences.bread_notes, data["bread_notes"])
#         self.assertEqual(food_preferences.salad, data["salad"])
#         self.assertEqual(food_preferences.salad_notes, data["salad_notes"])
#         self.assertEqual(food_preferences.soup, data["soup"])
#         self.assertEqual(food_preferences.soup_notes, data["soup_notes"])
#         self.assertEqual(food_preferences.cheese, data["cheese"])
#         self.assertEqual(food_preferences.cheese_notes, data["cheese_notes"])
#         self.assertEqual(food_preferences.dessert, data["dessert"])
#         self.assertEqual(food_preferences.dessert_notes, data["dessert_notes"])
#         self.assertEqual(food_preferences.kids_meals, data["kids_meals"])
#         self.assertEqual(food_preferences.kids_meals_notes, data["kids_meals_notes"])
#         self.assertEqual(food_preferences.kids_allergies, data["kids_allergies"])

#     def test_can_update_food_preferences(self):
#         food_preferences: FoodPreferences = FoodPreferencesFactory()

#         updated_data = {
#             "general_cuisine": FoodPreferences.GeneralCuisine.AMERICAN,
#             "general_cuisine_notes": "Note GC",
#             "fish_and_shellfish": FoodPreferences.FishAndShellfish.CLAMS,
#             "fish_and_shellfish_notes": "Note FS",
#             "meat": FoodPreferences.Meat.BEEF,
#             "meat_notes": "Note MT",
#             "bread": FoodPreferences.Bread.BAGEL,
#             "bread_notes": "Note BRD",
#             "salad": FoodPreferences.Salad.BRIOCHE,
#             "salad_notes": "Note SLD",
#             "soup": FoodPreferences.Soup.BORSCHT,
#             "soup_notes": "Note SOP",
#             "cheese": FoodPreferences.Cheese.BLUE,
#             "cheese_notes": "Note CHS",
#             "dessert": FoodPreferences.Dessert.CAKE,
#             "dessert_notes": "Note DSRT",
#             "kids_meals": KidsChoices.PIZZA,
#             "kids_meals_notes": "Note KIDSMEAL",
#             "kids_allergies": "allergies",
#         }

#         food_preferences: FoodPreferences = update_food_preferences(
#             food_preferences=food_preferences, **updated_data
#         )
#         food_preferences.refresh_from_db()

#         self.assertEquals(
#             updated_data["general_cuisine"], food_preferences.general_cuisine
#         )
#         self.assertEquals(
#             updated_data["general_cuisine_notes"],
#             food_preferences.general_cuisine_notes,
#         )
#         self.assertEquals(
#             updated_data["fish_and_shellfish"], food_preferences.fish_and_shellfish
#         )
#         self.assertEquals(
#             updated_data["fish_and_shellfish_notes"],
#             food_preferences.fish_and_shellfish_notes,
#         )
#         self.assertEquals(updated_data["meat"], food_preferences.meat)
#         self.assertEquals(updated_data["meat_notes"], food_preferences.meat_notes)
#         self.assertEquals(updated_data["bread"], food_preferences.bread)
#         self.assertEquals(updated_data["bread_notes"], food_preferences.bread_notes)
#         self.assertEquals(updated_data["salad"], food_preferences.salad)
#         self.assertEquals(updated_data["salad_notes"], food_preferences.salad_notes)
#         self.assertEquals(updated_data["soup"], food_preferences.soup)
#         self.assertEquals(updated_data["soup_notes"], food_preferences.soup_notes)
#         self.assertEquals(updated_data["cheese"], food_preferences.cheese)
#         self.assertEquals(updated_data["cheese_notes"], food_preferences.cheese_notes)
#         self.assertEquals(updated_data["dessert"], food_preferences.dessert)
#         self.assertEquals(updated_data["dessert_notes"], food_preferences.dessert_notes)
#         self.assertEquals(updated_data["kids_meals"], food_preferences.kids_meals)
#         self.assertEquals(
#             updated_data["kids_meals_notes"], food_preferences.kids_meals_notes
#         )
#         self.assertEquals(
#             updated_data["kids_allergies"], food_preferences.kids_allergies
#         )

#     def test_can_create_meal_and_room_preferences(self):
#         guest: GuestDetail = GuestFactory()

#         data = {
#             "guest": guest,
#             "breakfast_time": MealAndRoomPreferences.time_choices[0],
#             "breakfast_selection": BreakfastSelection.BreakfastSelection.ALFRESCO,
#             "breakfast_note": "Note Breakfast",
#             "lunch_time": MealAndRoomPreferences.time_choices[12],
#             "lunch_selection": LunchSelection.LunchSelection._2_COURSE,
#             "lunch_note": "Note Lunch",
#             "dinner_time": MealAndRoomPreferences.time_choices[13],
#             "dinner_selection": DinnerSelection.DinnerSelection._4_COURSE,
#             "dinner_note": "Note Dinner",
#             "canapes_time": MealAndRoomPreferences.CanapesTime.BEFORE_DINNER,
#             "canapes_selection": MealAndRoomPreferences.CanapesTypes.FULL_SELECTION,
#             "midmorning_snacks": MealAndRoomPreferences.MidMorningSnacks.SAVORY,
#             "midafternoon_snacks": MealAndRoomPreferences.MidAfternoonSnacks.SWEET,
#             "favorite_flowers": "Sunflower",
#         }

#         meal_and_room_preferences = create_meal_and_room_preferences(**data)

#         self.assertEqual(meal_and_room_preferences.guest, data["guest"])
#         self.assertEqual(
#             meal_and_room_preferences.breakfast_time, data["breakfast_time"]
#         )
#         self.assertEqual(
#             meal_and_room_preferences.breakfast_note, data["breakfast_note"]
#         )
#         self.assertEqual(meal_and_room_preferences.lunch_time, data["lunch_time"])
#         self.assertEqual(meal_and_room_preferences.lunch_note, data["lunch_note"])
#         self.assertEqual(meal_and_room_preferences.dinner_time, data["dinner_time"])
#         self.assertEqual(meal_and_room_preferences.dinner_note, data["dinner_note"])
#         self.assertEqual(meal_and_room_preferences.canapes_time, data["canapes_time"])
#         self.assertEqual(
#             meal_and_room_preferences.canapes_selection, data["canapes_selection"]
#         )
#         self.assertEqual(
#             meal_and_room_preferences.midmorning_snacks, data["midmorning_snacks"]
#         )
#         self.assertEqual(
#             meal_and_room_preferences.midafternoon_snacks, data["midafternoon_snacks"]
#         )
#         self.assertEqual(
#             meal_and_room_preferences.favorite_flowers, data["favorite_flowers"]
#         )

#     def test_can_update_meal_and_room_preferences(self):
#         meal_and_room_preferences: MealAndRoomPreferences = (
#             MealAndRoomPreferencesFactory(
#                 breakfast_selection=BreakfastSelectionFactory(),
#                 lunch_selection=LunchSelectionFactory(),
#                 dinner_selection=DinnerSelectionFactory(),
#             )
#         )

#         updated_data = {
#             "breakfast_time": MealAndRoomPreferences.time_choices[0],
#             "breakfast_selection": BreakfastSelection.BreakfastSelection.ALFRESCO,
#             "breakfast_note": "Note Breakfast",
#             "lunch_time": MealAndRoomPreferences.time_choices[12],
#             "lunch_selection": LunchSelection.LunchSelection._2_COURSE,
#             "lunch_note": "Note Lunch",
#             "dinner_time": MealAndRoomPreferences.time_choices[13],
#             "dinner_selection": DinnerSelection.DinnerSelection._4_COURSE,
#             "dinner_note": "Note Dinner",
#             "canapes_time": MealAndRoomPreferences.CanapesTime.BEFORE_DINNER,
#             "canapes_selection": MealAndRoomPreferences.CanapesTypes.FULL_SELECTION,
#             "midmorning_snacks": MealAndRoomPreferences.MidMorningSnacks.SAVORY,
#             "midafternoon_snacks": MealAndRoomPreferences.MidAfternoonSnacks.SWEET,
#             "favorite_flowers": "Sunflower",
#         }

#         meal_and_room_preferences: MealAndRoomPreferences = (
#             update_meal_and_room_preferences(
#                 meal_and_room_preferences=meal_and_room_preferences, **updated_data
#             )
#         )
#         meal_and_room_preferences.refresh_from_db()

#         self.assertEquals(
#             str(updated_data["breakfast_time"]),
#             meal_and_room_preferences.breakfast_time,
#         )
#         self.assertEquals(
#             updated_data["breakfast_note"], meal_and_room_preferences.breakfast_note
#         )
#         self.assertEquals(
#             str(updated_data["lunch_time"]), meal_and_room_preferences.lunch_time
#         )
#         self.assertEquals(
#             updated_data["lunch_note"], meal_and_room_preferences.lunch_note
#         )
#         self.assertEquals(
#             str(updated_data["dinner_time"]), meal_and_room_preferences.dinner_time
#         )
#         self.assertEquals(
#             updated_data["dinner_note"], meal_and_room_preferences.dinner_note
#         )
#         self.assertEquals(
#             updated_data["canapes_time"], meal_and_room_preferences.canapes_time
#         )
#         self.assertEquals(
#             updated_data["canapes_selection"],
#             meal_and_room_preferences.canapes_selection,
#         )
#         self.assertEquals(
#             updated_data["midmorning_snacks"],
#             meal_and_room_preferences.midmorning_snacks,
#         )
#         self.assertEquals(
#             updated_data["midafternoon_snacks"],
#             meal_and_room_preferences.midafternoon_snacks,
#         )
#         self.assertEquals(
#             updated_data["favorite_flowers"], meal_and_room_preferences.favorite_flowers
#         )

#     def test_can_create_diet_services_sizes_preferences(self):
#         guest: GuestDetail = GuestFactory()

#         data = {
#             "guest": guest,
#             "dietary_restrictions": DietServicesSizesPreferences.DietaryRestrictions.VEGETARIAN,
#             "dietary_restrictions_other_notes": "",
#             "dietary_restrictions_notes": "Note Dietary Restrictions",
#             "preferred_room_temperature": "27° C",
#             "other_services": DietServicesSizesPreferences.OtherServices.YOGA_INSTRUCTION,
#             "other_services_other_notes": "",
#             "shirt_sizing": DietServicesSizesPreferences.ShirtSizing.MENS,
#             "international_shirt_sizing": DietServicesSizesPreferences.InternationalShirtSizing.US,
#             "shirt_size": DietServicesSizesPreferences.ShirtSizes.M,
#             "shoe_sizing": DietServicesSizesPreferences.ShoeSizing.MENS,
#             "international_shoe_sizing": DietServicesSizesPreferences.InternationalShoeSizing.US,
#             "shoe_size": 10,
#         }

#         diet_services_sizes_preferences = create_diet_services_sizes_preferences(**data)

#         self.assertEqual(diet_services_sizes_preferences.guest, data["guest"])
#         self.assertEqual(
#             diet_services_sizes_preferences.dietary_restrictions,
#             data["dietary_restrictions"],
#         )
#         self.assertEqual(
#             diet_services_sizes_preferences.dietary_restrictions_other_notes,
#             data["dietary_restrictions_other_notes"],
#         )
#         self.assertEqual(
#             diet_services_sizes_preferences.dietary_restrictions_notes,
#             data["dietary_restrictions_notes"],
#         )
#         self.assertEqual(
#             diet_services_sizes_preferences.preferred_room_temperature,
#             data["preferred_room_temperature"],
#         )
#         self.assertEqual(
#             diet_services_sizes_preferences.other_services_other_notes,
#             data["other_services_other_notes"],
#         )
#         self.assertEqual(
#             diet_services_sizes_preferences.shirt_sizing, data["shirt_sizing"]
#         )
#         self.assertEqual(
#             diet_services_sizes_preferences.international_shirt_sizing,
#             data["international_shirt_sizing"],
#         )
#         self.assertEqual(diet_services_sizes_preferences.shirt_size, data["shirt_size"])
#         self.assertEqual(
#             diet_services_sizes_preferences.shoe_sizing, data["shoe_sizing"]
#         )
#         self.assertEqual(
#             diet_services_sizes_preferences.international_shoe_sizing,
#             data["international_shoe_sizing"],
#         )
#         self.assertEqual(diet_services_sizes_preferences.shoe_size, data["shoe_size"])

#     def test_can_update_diet_services_sizes_preferences(self):
#         diet_services_sizes_preferences: DietServicesSizesPreferences = (
#             DietServicesSizesPreferencesFactory(other_service=OtherServicesFactory())
#         )

#         updated_data = {
#             "dietary_restrictions": DietServicesSizesPreferences.DietaryRestrictions.VEGETARIAN,
#             "dietary_restrictions_other_notes": "",
#             "dietary_restrictions_notes": "Note Dietary Restrictions",
#             "preferred_room_temperature": "27° C",
#             "other_services": DietServicesSizesPreferences.OtherServices.YOGA_INSTRUCTION,
#             "other_services_other_notes": "",
#             "shirt_sizing": DietServicesSizesPreferences.ShirtSizing.MENS,
#             "international_shirt_sizing": DietServicesSizesPreferences.InternationalShirtSizing.US,
#             "shirt_size": DietServicesSizesPreferences.ShirtSizes.M,
#             "shoe_sizing": DietServicesSizesPreferences.ShoeSizing.MENS,
#             "international_shoe_sizing": DietServicesSizesPreferences.InternationalShoeSizing.US,
#             "shoe_size": 10,
#         }

#         diet_services_sizes_preferences: DietServicesSizesPreferences = (
#             update_diet_services_sizes_preferences(
#                 diet_services_sizes_preferences=diet_services_sizes_preferences,
#                 **updated_data
#             )
#         )
#         diet_services_sizes_preferences.refresh_from_db()

#         self.assertEquals(
#             updated_data["dietary_restrictions"],
#             diet_services_sizes_preferences.dietary_restrictions,
#         )
#         self.assertEquals(
#             updated_data["dietary_restrictions_other_notes"],
#             diet_services_sizes_preferences.dietary_restrictions_other_notes,
#         )
#         self.assertEquals(
#             updated_data["dietary_restrictions_notes"],
#             diet_services_sizes_preferences.dietary_restrictions_notes,
#         )
#         self.assertEquals(
#             updated_data["preferred_room_temperature"],
#             diet_services_sizes_preferences.preferred_room_temperature,
#         )
#         self.assertEquals(
#             updated_data["other_services_other_notes"],
#             diet_services_sizes_preferences.other_services_other_notes,
#         )
#         self.assertEquals(
#             updated_data["shirt_sizing"], diet_services_sizes_preferences.shirt_sizing
#         )
#         self.assertEquals(
#             updated_data["international_shirt_sizing"],
#             diet_services_sizes_preferences.international_shirt_sizing,
#         )
#         self.assertEquals(
#             updated_data["shirt_size"],
#             diet_services_sizes_preferences.shirt_size,
#         )
#         self.assertEquals(
#             updated_data["shoe_sizing"],
#             diet_services_sizes_preferences.shoe_sizing,
#         )
#         self.assertEquals(
#             updated_data["international_shoe_sizing"],
#             diet_services_sizes_preferences.international_shoe_sizing,
#         )
#         self.assertEquals(
#             updated_data["shoe_size"], diet_services_sizes_preferences.shoe_size
#         )

#     def test_can_create_beverages_alcohol_preferences(self):
#         guest: GuestDetail = GuestFactory()

#         data = {
#             "guest": guest,
#             "milk_selection": BeveragesAndAlcoholicPreferences.MilkSelections.SOYA,
#             "milk_note": "milk note",
#             "coffee_selection": BeveragesAndAlcoholicPreferences.CoffeeSelections.ICED_COFFEE,
#             "coffee_note": "coffe note",
#             "tea_selection": BeveragesAndAlcoholicPreferences.TeaSelections.HERBAL_TEA,
#             "tea_note": "tea note",
#             "water_selection": BeveragesAndAlcoholicPreferences.WaterSelections.SPARKLING,
#             "water_note": "water note",
#             "juice_selection": BeveragesAndAlcoholicPreferences.JuiceSelections.FRESH_PINEAPPLE,
#             "juice_note": "juice note",
#             "sodas_and_mixers_selection": BeveragesAndAlcoholicPreferences.SodasMixersSelections.TONIC,
#             "sodas_and_mixers_note": "sodas and mixers note",
#             "add_ons_selection": BeveragesAndAlcoholicPreferences.AddOnsSelections.SWEETENER,
#             "add_ons_note": "ad ons note",
#             "whiskey_name": "Whiskey Brand",
#             "whiskey_quantity": 10,
#             "brandy_name": "Brandy Brand",
#             "brandy_quantity": 10,
#             "vodka_name": "Vodka Brand",
#             "vodka_quantity": 10,
#             "tequila_name": "Tequila Brand",
#             "tequila_quantity": 10,
#             "rum_name": "Rum Brand",
#             "rum_quantity": 10,
#             "liquors_name": "Liquor Brand",
#             "liquors_quantity": 10,
#             "cocktail_name": "Cocktail Brand",
#             "cocktail_quantity": 10,
#             "port_beer_name": "Port/Beer Brand",
#             "port_beer_quantity": 10,
#             "red_wine_name": "Red Wine Brand",
#             "red_wine_quantity": 10,
#             "white_wine_name": "White Wine Brand",
#             "white_wine_quantity": 10,
#             "champagne_name": "Champagne Brand",
#             "champagne_quantity": 10,
#             "other_name": "Other Alcohol",
#             "other_quantity": 10,
#         }

#         beverages_and_alcoholic_preferences = create_beverages_alcohol_preferences(
#             **data
#         )

#         self.assertEqual(beverages_and_alcoholic_preferences.guest, data["guest"])
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.milk_note, data["milk_note"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.coffee_note, data["coffee_note"]
#         )
#         self.assertEqual(beverages_and_alcoholic_preferences.tea_note, data["tea_note"])
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.water_note, data["water_note"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.juice_note, data["juice_note"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.sodas_and_mixers_note,
#             data["sodas_and_mixers_note"],
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.add_ons_note, data["add_ons_note"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.whiskey_name, data["whiskey_name"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.white_wine_quantity,
#             data["white_wine_quantity"],
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.brandy_name, data["brandy_name"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.brandy_quantity, data["brandy_quantity"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.vodka_name, data["vodka_name"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.vodka_quantity, data["vodka_quantity"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.tequila_name, data["tequila_name"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.tequila_quantity,
#             data["tequila_quantity"],
#         )
#         self.assertEqual(beverages_and_alcoholic_preferences.rum_name, data["rum_name"])
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.rum_quantity, data["rum_quantity"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.liquors_name, data["liquors_name"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.liquors_quantity,
#             data["liquors_quantity"],
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.cocktail_name, data["cocktail_name"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.cocktail_quantity,
#             data["cocktail_quantity"],
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.port_beer_name, data["port_beer_name"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.port_beer_quantity,
#             data["port_beer_quantity"],
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.red_wine_name, data["red_wine_name"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.red_wine_quantity,
#             data["red_wine_quantity"],
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.white_wine_quantity,
#             data["white_wine_quantity"],
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.white_wine_quantity,
#             data["white_wine_quantity"],
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.champagne_name, data["champagne_name"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.champagne_quantity,
#             data["champagne_quantity"],
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.other_name, data["other_name"]
#         )
#         self.assertEqual(
#             beverages_and_alcoholic_preferences.other_quantity, data["other_quantity"]
#         )

#     def test_can_update_beverages_alcohol_preferences(self):
#         beverages_and_alcoholic_preferences: BeveragesAndAlcoholicPreferences = (
#             BeveragesAndAlcoholicPreferencesFactory(
#                 milk_selection=MilkSelectionFactory(),
#                 coffee_selection=CoffeeSelectionFactory(),
#                 tea_selection=TeaSelectionFactory(),
#                 water_selection=WaterSelectionFactory(),
#                 juice_selection=JuiceSelectionFactory(),
#                 sodas_and_mixers_selection=SodasAndMixersSelectionFactory(),
#                 add_ons_selection=AddOnsSelectionFactory(),
#             )
#         )
#         updated_data = {
#             "milk_selection": [
#                 BeveragesAndAlcoholicPreferences.MilkSelections.SOYA.value
#             ],
#             "milk_note": "milk note",
#             "coffee_selection": [
#                 BeveragesAndAlcoholicPreferences.CoffeeSelections.ICED_COFFEE.value
#             ],
#             "coffee_note": "coffe note",
#             "tea_selection": [
#                 BeveragesAndAlcoholicPreferences.TeaSelections.HERBAL_TEA.value
#             ],
#             "tea_note": "tea note",
#             "water_selection": [
#                 BeveragesAndAlcoholicPreferences.WaterSelections.SPARKLING.value
#             ],
#             "water_note": "water note",
#             "juice_selection": [
#                 BeveragesAndAlcoholicPreferences.JuiceSelections.FRESH_PINEAPPLE.value
#             ],
#             "juice_note": "juice note",
#             "sodas_and_mixers_selection": [
#                 BeveragesAndAlcoholicPreferences.SodasMixersSelections.TONIC.value
#             ],
#             "sodas_and_mixers_note": "sodas and mixers note",
#             "add_ons_selection": [
#                 BeveragesAndAlcoholicPreferences.AddOnsSelections.SWEETENER.value
#             ],
#             "add_ons_note": "ad ons note",
#             "whiskey_name": "Whiskey Brand",
#             "whiskey_quantity": 10,
#             "brandy_name": "Brandy Brand",
#             "brandy_quantity": 10,
#             "vodka_name": "Vodka Brand",
#             "vodka_quantity": 10,
#             "tequila_name": "Tequila Brand",
#             "tequila_quantity": 10,
#             "rum_name": "Rum Brand",
#             "rum_quantity": 10,
#             "liquors_name": "Liquor Brand",
#             "liquors_quantity": 10,
#             "cocktail_name": "Cocktail Brand",
#             "cocktail_quantity": 10,
#             "port_beer_name": "Port/Beer Brand",
#             "port_beer_quantity": 10,
#             "red_wine_name": "Red Wine Brand",
#             "red_wine_quantity": 10,
#             "white_wine_name": "White Wine Brand",
#             "white_wine_quantity": 10,
#             "champagne_name": "Champagne Brand",
#             "champagne_quantity": 10,
#             "other_name": "Other Alcohol",
#             "other_quantity": 10,
#         }

#         beverages_and_alcoholic_preferences: BeveragesAndAlcoholicPreferences = (
#             update_beverages_alcohol_preferences(
#                 beverages_and_alcoholic_preferences=beverages_and_alcoholic_preferences,
#                 **updated_data
#             )
#         )
#         beverages_and_alcoholic_preferences.refresh_from_db()

#         self.assertEquals(
#             beverages_and_alcoholic_preferences.milk_note, updated_data["milk_note"]
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.coffee_note, updated_data["coffee_note"]
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.tea_note, updated_data["tea_note"]
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.water_note, updated_data["water_note"]
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.juice_note, updated_data["juice_note"]
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.sodas_and_mixers_note,
#             updated_data["sodas_and_mixers_note"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.add_ons_note,
#             updated_data["add_ons_note"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.whiskey_name,
#             updated_data["whiskey_name"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.whiskey_quantity,
#             updated_data["whiskey_quantity"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.brandy_name, updated_data["brandy_name"]
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.brandy_quantity,
#             updated_data["brandy_quantity"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.vodka_name, updated_data["vodka_name"]
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.vodka_quantity,
#             updated_data["vodka_quantity"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.tequila_name,
#             updated_data["tequila_name"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.tequila_quantity,
#             updated_data["tequila_quantity"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.rum_name, updated_data["rum_name"]
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.rum_quantity,
#             updated_data["rum_quantity"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.liquors_name,
#             updated_data["liquors_name"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.liquors_quantity,
#             updated_data["liquors_quantity"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.cocktail_name,
#             updated_data["cocktail_name"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.cocktail_quantity,
#             updated_data["cocktail_quantity"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.port_beer_name,
#             updated_data["port_beer_name"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.port_beer_quantity,
#             updated_data["port_beer_quantity"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.red_wine_name,
#             updated_data["red_wine_name"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.red_wine_quantity,
#             updated_data["red_wine_quantity"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.white_wine_quantity,
#             updated_data["white_wine_quantity"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.white_wine_quantity,
#             updated_data["white_wine_quantity"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.champagne_name,
#             updated_data["champagne_name"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.champagne_quantity,
#             updated_data["champagne_quantity"],
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.other_name, updated_data["other_name"]
#         )
#         self.assertEquals(
#             beverages_and_alcoholic_preferences.other_quantity,
#             updated_data["other_quantity"],
#         )
