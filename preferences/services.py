from charter.models import (
    AddOnsSelection,
    BeveragesAndAlcoholicPreferences,
    BreakfastSelection,
    CoffeeSelection,
    DietServicesSizesPreferences,
    DinnerSelection,
    FoodPreferences,
    GuestDetail,
    JuiceSelection,
    LunchSelection,
    MealAndRoomPreferences,
    MilkSelection,
    OtherServices,
    SodasAndMixersSelection,
    TeaSelection,
    WaterSelection,
)
from authentication.models import User
from preferences.models import ShortJetPreferenceSheet, LongJetPreferenceSheet


def create_food_preferences(
    *,
    guest: User,
    general_cuisine: str,
    general_cuisine_notes: str,
    fish_and_shellfish: str,
    fish_and_shellfish_notes: str,
    meat: str,
    meat_notes: str,
    bread: str,
    bread_notes: str,
    salad: str,
    salad_notes: str,
    soup: str,
    soup_notes: str,
    cheese: str,
    cheese_notes: str,
    dessert: str,
    dessert_notes: str,
    kids_meals: str,
    kids_meals_notes: str,
    kids_allergies: str,
) -> FoodPreferences:
    """
    Creates food preferences of principal guest
    """
    food_preferences = FoodPreferences.objects.create(
        guest=guest,
        general_cuisine=general_cuisine,
        general_cuisine_notes=general_cuisine_notes,
        fish_and_shellfish=fish_and_shellfish,
        fish_and_shellfish_notes=fish_and_shellfish_notes,
        meat=meat,
        meat_notes=meat_notes,
        bread=bread,
        bread_notes=bread_notes,
        salad=salad,
        salad_notes=salad_notes,
        soup=soup,
        soup_notes=soup_notes,
        cheese=cheese,
        cheese_notes=cheese_notes,
        dessert=dessert,
        dessert_notes=dessert_notes,
        kids_meals=kids_meals,
        kids_meals_notes=kids_meals_notes,
        kids_allergies=kids_allergies,
    )

    return food_preferences


def update_food_preferences(
    *,
    food_preferences: FoodPreferences,
    general_cuisine: str,
    general_cuisine_notes: str,
    fish_and_shellfish: str,
    fish_and_shellfish_notes: str,
    meat: str,
    meat_notes: str,
    bread: str,
    bread_notes: str,
    salad: str,
    salad_notes: str,
    soup: str,
    soup_notes: str,
    cheese: str,
    cheese_notes: str,
    dessert: str,
    dessert_notes: str,
    kids_meals: str,
    kids_meals_notes: str,
    kids_allergies: str,
):
    """
    Update food preferences of principal guest
    """
    food_preferences.general_cuisine = general_cuisine
    food_preferences.general_cuisine_notes = general_cuisine_notes
    food_preferences.fish_and_shellfish = fish_and_shellfish
    food_preferences.fish_and_shellfish_notes = fish_and_shellfish_notes
    food_preferences.meat = meat
    food_preferences.meat_notes = meat_notes
    food_preferences.bread = bread
    food_preferences.bread_notes = bread_notes
    food_preferences.salad = salad
    food_preferences.salad_notes = salad_notes
    food_preferences.soup = soup
    food_preferences.soup_notes = soup_notes
    food_preferences.cheese = cheese
    food_preferences.cheese_notes = cheese_notes
    food_preferences.dessert = dessert
    food_preferences.dessert_notes = dessert_notes
    food_preferences.kids_meals = kids_meals
    food_preferences.kids_meals_notes = kids_meals_notes
    food_preferences.kids_allergies = kids_allergies

    food_preferences.save()

    return food_preferences


def create_meal_and_room_preferences(
    *,
    guest: User,
    dietary_restrictions: str,
    dietary_restrictions_other_notes: str,
    dietary_restrictions_notes: str,
    breakfast_time: str,
    breakfast_selection: str,
    breakfast_note: str,
    lunch_time: str,
    lunch_selection: str,
    lunch_note: str,
    dinner_time: str,
    dinner_selection: str,
    dinner_note: str,
    canapes_time: str,
    canapes_selection: str,
    midmorning_snacks: str,
    midafternoon_snacks: str,
) -> MealAndRoomPreferences:
    """
    Creates meal and food preferences of principal guest
    """
    meal_and_room_preferences = MealAndRoomPreferences.objects.create(
        guest=guest,
        dietary_restrictions=dietary_restrictions,
        dietary_restrictions_other_notes=dietary_restrictions_other_notes,
        dietary_restrictions_notes=dietary_restrictions_notes,
        breakfast_time=breakfast_time,
        breakfast_note=breakfast_note,
        lunch_time=lunch_time,
        lunch_note=lunch_note,
        dinner_time=dinner_time,
        dinner_note=dinner_note,
        canapes_time=canapes_time,
        canapes_selection=canapes_selection,
        midmorning_snacks=midmorning_snacks,
        midafternoon_snacks=midafternoon_snacks,
    )

    breakfast_selection = BreakfastSelection.objects.create(
        name=breakfast_selection, meal_and_room_preference=meal_and_room_preferences
    )
    lunch_selection = LunchSelection.objects.create(
        name=lunch_selection, meal_and_room_preference=meal_and_room_preferences
    )
    dinner_selection = DinnerSelection.objects.create(
        name=dinner_selection, meal_and_room_preference=meal_and_room_preferences
    )

    return meal_and_room_preferences


def update_meal_and_room_preferences(
    *,
    meal_and_room_preferences: MealAndRoomPreferences,
    dietary_restrictions: str,
    dietary_restrictions_other_notes: str,
    dietary_restrictions_notes: str,
    breakfast_selection: str,
    lunch_selection: str,
    dinner_selection: str,
    breakfast_time: str,
    breakfast_note: str,
    lunch_time: str,
    lunch_note: str,
    dinner_time: str,
    dinner_note: str,
    canapes_time: str,
    canapes_selection: str,
    midmorning_snacks: str,
    midafternoon_snacks: str,
):
    """
    Update meal and room preferences of principal guest
    """
    meal_and_room_preferences.dietary_restrictions = dietary_restrictions
    meal_and_room_preferences.dietary_restrictions_other_notes = (
        dietary_restrictions_other_notes
    )
    meal_and_room_preferences.dietary_restrictions_notes = dietary_restrictions_notes
    meal_and_room_preferences.breakfast_time = breakfast_time
    meal_and_room_preferences.breakfast_note = breakfast_note
    meal_and_room_preferences.lunch_time = lunch_time
    meal_and_room_preferences.lunch_note = lunch_note
    meal_and_room_preferences.dinner_time = dinner_time
    meal_and_room_preferences.dinner_note = dinner_note
    meal_and_room_preferences.canapes_time = canapes_time
    meal_and_room_preferences.canapes_selection = canapes_selection
    meal_and_room_preferences.midmorning_snacks = midmorning_snacks
    meal_and_room_preferences.midafternoon_snacks = midafternoon_snacks
    meal_and_room_preferences.save()

    instance_breakfast_selection = meal_and_room_preferences.breakfast_selection
    instance_lunch_selection = meal_and_room_preferences.lunch_selection
    instance_dinner_selection = meal_and_room_preferences.dinner_selection
    instance_breakfast_selection.name = breakfast_selection
    instance_lunch_selection.name = lunch_selection
    instance_dinner_selection.name = dinner_selection
    instance_breakfast_selection.save()
    instance_lunch_selection.save()
    instance_dinner_selection.save()

    return meal_and_room_preferences


def create_diet_services_sizes_preferences(
    *,
    guest: User,
    preferred_room_temperature: str,
    other_services: str,
    other_services_other_notes: str,
    shirt_sizing: str,
    international_shirt_sizing: str,
    shirt_size: str,
    shoe_sizing: str,
    international_shoe_sizing: str,
    shoe_size: str,
    favorite_flowers: str,
) -> DietServicesSizesPreferences:
    """
    Creates diet, services and sizes of all guests
    """
    diet_services_sizes_preferences = DietServicesSizesPreferences.objects.create(
        guest=guest,
        preferred_room_temperature=preferred_room_temperature,
        other_services_other_notes=other_services_other_notes,
        shirt_sizing=shirt_sizing,
        international_shirt_sizing=international_shirt_sizing,
        shirt_size=shirt_size,
        shoe_sizing=shoe_sizing,
        international_shoe_sizing=international_shoe_sizing,
        shoe_size=shoe_size,
        favorite_flowers=favorite_flowers,
    )

    other_services = OtherServices.objects.create(
        name=other_services,
        diet_services_sizes_preferences=diet_services_sizes_preferences,
    )

    return diet_services_sizes_preferences


def update_diet_services_sizes_preferences(
    *,
    diet_services_sizes_preferences: DietServicesSizesPreferences,
    preferred_room_temperature: str,
    other_services: str,
    other_services_other_notes: str,
    shirt_sizing: str,
    international_shirt_sizing: str,
    shirt_size: str,
    shoe_sizing: str,
    international_shoe_sizing: str,
    shoe_size: str,
    favorite_flowers: str,
):
    """
    Update diet, service and sizes preferences of all guests
    """
    diet_services_sizes_preferences.preferred_room_temperature = (
        preferred_room_temperature
    )
    diet_services_sizes_preferences.other_services_other_notes = (
        other_services_other_notes
    )
    diet_services_sizes_preferences.shirt_sizing = shirt_sizing
    diet_services_sizes_preferences.international_shirt_sizing = (
        international_shirt_sizing
    )
    diet_services_sizes_preferences.shirt_size = shirt_size
    diet_services_sizes_preferences.shoe_sizing = shoe_sizing
    diet_services_sizes_preferences.international_shoe_sizing = (
        international_shoe_sizing
    )
    diet_services_sizes_preferences.shoe_size = shoe_size
    diet_services_sizes_preferences.favorite_flowers = favorite_flowers
    diet_services_sizes_preferences.save()

    instance_other_services = diet_services_sizes_preferences.other_service
    instance_other_services.name = other_services
    instance_other_services.save()

    return diet_services_sizes_preferences


def create_beverages_alcohol_preferences(
    *,
    guest: User,
    milk_selection: str,
    milk_note: str,
    coffee_selection: str,
    coffee_note: str,
    tea_selection: str,
    tea_note: str,
    water_selection: str,
    water_note: str,
    juice_selection: str,
    juice_note: str,
    sodas_and_mixers_selection: str,
    sodas_and_mixers_note: str,
    add_ons_selection: str,
    add_ons_note: str,
    whiskey_name: str,
    whiskey_quantity: int,
    extra_whiskey: dict,
    brandy_name: str,
    brandy_quantity: int,
    extra_brandy: dict,
    vodka_name: str,
    vodka_quantity: int,
    extra_vodka: dict,
    tequila_name: str,
    tequila_quantity: int,
    extra_tequila: dict,
    rum_name: str,
    rum_quantity: int,
    extra_rum: dict,
    liquors_name: str,
    liquors_quantity: int,
    extra_liquors: dict,
    cocktail_name: str,
    cocktail_quantity: int,
    extra_cocktail: dict,
    port_beer_name: str,
    port_beer_quantity: int,
    extra_port_beer: dict,
    red_wine_name: str,
    red_wine_quantity: int,
    extra_red_wine: dict,
    white_wine_name: str,
    white_wine_quantity: int,
    extra_white_wine: dict,
    rose_wine_name: str,
    rose_wine_quantity: int,
    extra_rose_wine: dict,
    champagne_name: str,
    champagne_quantity: int,
    extra_champagne: dict,
    other_name: str,
    other_quantity: int,
) -> BeveragesAndAlcoholicPreferences:
    """
    Creates beverages and alcohol preferences for all guests
    """
    beverages_and_alcoholic_preferences = (
        BeveragesAndAlcoholicPreferences.objects.create(
            guest=guest,
            milk_note=milk_note,
            coffee_note=coffee_note,
            tea_note=tea_note,
            water_note=water_note,
            juice_note=juice_note,
            sodas_and_mixers_note=sodas_and_mixers_note,
            add_ons_note=add_ons_note,
            whiskey_name=whiskey_name,
            whiskey_quantity=whiskey_quantity,
            extra_whiskey=extra_whiskey,
            brandy_name=brandy_name,
            brandy_quantity=brandy_quantity,
            extra_brandy=extra_brandy,
            vodka_name=vodka_name,
            vodka_quantity=vodka_quantity,
            extra_vodka=extra_vodka,
            tequila_name=tequila_name,
            tequila_quantity=tequila_quantity,
            extra_tequila=extra_tequila,
            rum_name=rum_name,
            rum_quantity=rum_quantity,
            extra_rum=extra_rum,
            liquors_name=liquors_name,
            liquors_quantity=liquors_quantity,
            extra_liquors=extra_liquors,
            cocktail_name=cocktail_name,
            cocktail_quantity=cocktail_quantity,
            extra_cocktail=extra_cocktail,
            port_beer_name=port_beer_name,
            port_beer_quantity=port_beer_quantity,
            extra_port_beer=extra_port_beer,
            red_wine_name=red_wine_name,
            red_wine_quantity=red_wine_quantity,
            extra_red_wine=extra_red_wine,
            white_wine_name=white_wine_name,
            white_wine_quantity=white_wine_quantity,
            extra_white_wine=extra_white_wine,
            rose_wine_name=rose_wine_name,
            rose_wine_quantity=rose_wine_quantity,
            extra_rose_wine=extra_rose_wine,
            champagne_name=champagne_name,
            champagne_quantity=champagne_quantity,
            extra_champagne=extra_champagne,
            other_name=other_name,
            other_quantity=other_quantity,
        )
    )

    milk_selection = MilkSelection.objects.create(
        name=milk_selection,
        beverages_and_alcoholic_preferences=beverages_and_alcoholic_preferences,
    )
    coffee_selection = CoffeeSelection.objects.create(
        name=coffee_selection,
        beverages_and_alcoholic_preferences=beverages_and_alcoholic_preferences,
    )
    tea_selection = TeaSelection.objects.create(
        name=tea_selection,
        beverages_and_alcoholic_preferences=beverages_and_alcoholic_preferences,
    )
    water_selection = WaterSelection.objects.create(
        name=water_selection,
        beverages_and_alcoholic_preferences=beverages_and_alcoholic_preferences,
    )
    juice_selection = JuiceSelection.objects.create(
        name=juice_selection,
        beverages_and_alcoholic_preferences=beverages_and_alcoholic_preferences,
    )
    sodas_and_mixers_selection = SodasAndMixersSelection.objects.create(
        name=sodas_and_mixers_selection,
        beverages_and_alcoholic_preferences=beverages_and_alcoholic_preferences,
    )
    add_ons_selection = AddOnsSelection.objects.create(
        name=add_ons_selection,
        beverages_and_alcoholic_preferences=beverages_and_alcoholic_preferences,
    )

    return beverages_and_alcoholic_preferences


def update_beverages_alcohol_preferences(
    *,
    beverages_and_alcoholic_preferences: BeveragesAndAlcoholicPreferences,
    milk_selection: str,
    milk_note: str,
    coffee_selection: str,
    coffee_note: str,
    tea_selection: str,
    tea_note: str,
    water_selection: str,
    water_note: str,
    juice_selection: str,
    juice_note: str,
    sodas_and_mixers_selection: str,
    sodas_and_mixers_note: str,
    add_ons_selection: str,
    add_ons_note: str,
    whiskey_name: str,
    whiskey_quantity: int,
    extra_whiskey: dict,
    brandy_name: str,
    brandy_quantity: int,
    extra_brandy: dict,
    vodka_name: str,
    vodka_quantity: int,
    extra_vodka: dict,
    tequila_name: str,
    tequila_quantity: int,
    extra_tequila: dict,
    rum_name: str,
    rum_quantity: int,
    extra_rum: dict,
    liquors_name: str,
    liquors_quantity: int,
    extra_liquors: dict,
    cocktail_name: str,
    cocktail_quantity: int,
    extra_cocktail: dict,
    port_beer_name: str,
    port_beer_quantity: int,
    extra_port_beer: dict,
    red_wine_name: str,
    red_wine_quantity: int,
    extra_red_wine: dict,
    white_wine_name: str,
    white_wine_quantity: int,
    extra_white_wine: dict,
    rose_wine_name: str,
    rose_wine_quantity: int,
    extra_rose_wine: dict,
    champagne_name: str,
    champagne_quantity: int,
    extra_champagne: dict,
    other_name: str,
    other_quantity: int,
):
    """
    Update beverages and alcohol preferences of all guests
    """
    beverages_and_alcoholic_preferences.milk_note = milk_note
    beverages_and_alcoholic_preferences.coffee_note = coffee_note
    beverages_and_alcoholic_preferences.tea_note = tea_note
    beverages_and_alcoholic_preferences.water_note = water_note
    beverages_and_alcoholic_preferences.juice_note = juice_note
    beverages_and_alcoholic_preferences.sodas_and_mixers_note = sodas_and_mixers_note
    beverages_and_alcoholic_preferences.add_ons_note = add_ons_note
    beverages_and_alcoholic_preferences.whiskey_name = whiskey_name
    beverages_and_alcoholic_preferences.whiskey_quantity = whiskey_quantity
    beverages_and_alcoholic_preferences.brandy_name = brandy_name
    beverages_and_alcoholic_preferences.brandy_quantity = brandy_quantity
    beverages_and_alcoholic_preferences.vodka_name = vodka_name
    beverages_and_alcoholic_preferences.vodka_quantity = vodka_quantity
    beverages_and_alcoholic_preferences.tequila_name = tequila_name
    beverages_and_alcoholic_preferences.tequila_quantity = tequila_quantity
    beverages_and_alcoholic_preferences.rum_name = rum_name
    beverages_and_alcoholic_preferences.rum_quantity = rum_quantity
    beverages_and_alcoholic_preferences.brandy_name = brandy_name
    beverages_and_alcoholic_preferences.brandy_quantity = brandy_quantity
    beverages_and_alcoholic_preferences.liquors_name = liquors_name
    beverages_and_alcoholic_preferences.liquors_quantity = liquors_quantity
    beverages_and_alcoholic_preferences.cocktail_name = cocktail_name
    beverages_and_alcoholic_preferences.cocktail_quantity = cocktail_quantity
    beverages_and_alcoholic_preferences.port_beer_name = port_beer_name
    beverages_and_alcoholic_preferences.port_beer_quantity = port_beer_quantity
    beverages_and_alcoholic_preferences.red_wine_name = red_wine_name
    beverages_and_alcoholic_preferences.red_wine_quantity = red_wine_quantity
    beverages_and_alcoholic_preferences.white_wine_name = white_wine_name
    beverages_and_alcoholic_preferences.white_wine_quantity = white_wine_quantity
    beverages_and_alcoholic_preferences.rose_wine_name = rose_wine_name
    beverages_and_alcoholic_preferences.rose_wine_quantity = rose_wine_quantity
    beverages_and_alcoholic_preferences.champagne_name = champagne_name
    beverages_and_alcoholic_preferences.champagne_quantity = champagne_quantity
    beverages_and_alcoholic_preferences.other_name = other_name
    beverages_and_alcoholic_preferences.other_quantity = other_quantity
    beverages_and_alcoholic_preferences.extra_whiskey = extra_whiskey
    beverages_and_alcoholic_preferences.extra_brandy = extra_brandy
    beverages_and_alcoholic_preferences.extra_vodka = extra_vodka
    beverages_and_alcoholic_preferences.extra_tequila = extra_tequila
    beverages_and_alcoholic_preferences.extra_rum = extra_rum
    beverages_and_alcoholic_preferences.extra_liquors = extra_liquors
    beverages_and_alcoholic_preferences.extra_cocktail = extra_cocktail
    beverages_and_alcoholic_preferences.extra_port_beer = extra_port_beer
    beverages_and_alcoholic_preferences.extra_red_wine = extra_red_wine
    beverages_and_alcoholic_preferences.extra_white_wine = extra_white_wine
    beverages_and_alcoholic_preferences.extra_rose_wine = extra_rose_wine
    beverages_and_alcoholic_preferences.extra_champagne = extra_champagne
    beverages_and_alcoholic_preferences.save()

    instance_milk_selection = beverages_and_alcoholic_preferences.milk_selection
    instance_coffee_selection = beverages_and_alcoholic_preferences.coffee_selection
    instance_tea_selection = beverages_and_alcoholic_preferences.tea_selection
    instance_water_selection = beverages_and_alcoholic_preferences.water_selection
    instance_juice_selection = beverages_and_alcoholic_preferences.juice_selection
    instance_sodas_and_mixers_selection = (
        beverages_and_alcoholic_preferences.sodas_and_mixers_selection
    )
    instance_add_ons_selection = beverages_and_alcoholic_preferences.add_ons_selection

    instance_milk_selection.name = milk_selection
    instance_coffee_selection.name = coffee_selection
    instance_tea_selection.name = tea_selection
    instance_water_selection.name = water_selection
    instance_juice_selection.name = juice_selection
    instance_sodas_and_mixers_selection.name = sodas_and_mixers_selection
    instance_add_ons_selection.name = add_ons_selection

    instance_milk_selection.save()
    instance_coffee_selection.save()
    instance_tea_selection.save()
    instance_water_selection.save()
    instance_juice_selection.save()
    instance_sodas_and_mixers_selection.save()
    instance_add_ons_selection.save()

    return beverages_and_alcoholic_preferences


def create_short_jet_preferences(
    *,
    guest: GuestDetail,
    dietary_restrictions: str,
    dietary_restrictions_notes: str,
    dietary_restrictions_other_notes: str,
    breakfast: str,
    breakfast_notes: str,
    lunch: str,
    lunch_notes: str,
    dinner: str,
    dinner_notes: str,
    kids_meals: str,
    kids_allergies: str,
    kids_meals_notes: str,
    favorite_flowers: str,
) -> ShortJetPreferenceSheet:
    """
    Creates Short Jet Preferences
    """
    short_jet_preference = ShortJetPreferenceSheet.objects.create(
        guest=guest,
        dietary_restrictions=dietary_restrictions,
        dietary_restrictions_notes=dietary_restrictions_notes,
        dietary_restrictions_other_notes=dietary_restrictions_other_notes,
        breakfast=breakfast,
        breakfast_notes=breakfast_notes,
        lunch=lunch,
        lunch_notes=lunch_notes,
        dinner=dinner,
        dinner_notes=dinner_notes,
        kids_meals=kids_meals,
        kids_allergies=kids_allergies,
        kids_meals_notes=kids_meals_notes,
        favorite_flowers=favorite_flowers,
    )

    return short_jet_preference


def update_short_jet_preferences(
    *,
    instance: ShortJetPreferenceSheet,
    dietary_restrictions: str,
    dietary_restrictions_notes: str,
    dietary_restrictions_other_notes: str,
    breakfast: str,
    breakfast_notes: str,
    lunch: str,
    lunch_notes: str,
    dinner: str,
    dinner_notes: str,
    kids_meals: str,
    kids_allergies: str,
    kids_meals_notes: str,
    favorite_flowers: str,
) -> ShortJetPreferenceSheet:
    """
    Updates Short Jet Preferences
    """

    instance.dietary_restrictions = dietary_restrictions
    instance.dietary_restrictions_notes = dietary_restrictions_notes
    instance.dietary_restrictions_other_notes = dietary_restrictions_other_notes
    instance.breakfast = breakfast
    instance.breakfast_notes = breakfast_notes
    instance.lunch = lunch
    instance.lunch_notes = lunch_notes
    instance.dinner = dinner
    instance.dinner_notes = dinner_notes
    instance.kids_meals = kids_meals
    instance.kids_allergies = kids_allergies
    instance.kids_meals_notes = kids_meals_notes
    instance.favorite_flowers = favorite_flowers

    instance.save()

    return instance


def create_long_jet_preferences(
    *,
    guest: GuestDetail,
    dietary_restrictions: str,
    dietary_restrictions_notes: str,
    dietary_restrictions_other_notes: str,
    breakfast: str,
    breakfast_notes: str,
    lunch: str,
    lunch_notes: str,
    dinner: str,
    dinner_notes: str,
    fresh_snacks: str,
    fresh_snacks_notes: str,
    pantry_snacks: str,
    pantry_snacks_notes: str,
    kids_meals: str,
    kids_allergies: str,
    kids_meals_notes: str,
    favorite_flowers: str,
) -> ShortJetPreferenceSheet:
    """
    Creates Long Jet Preferences
    """
    long_jet_preference = LongJetPreferenceSheet.objects.create(
        guest=guest,
        dietary_restrictions=dietary_restrictions,
        dietary_restrictions_notes=dietary_restrictions_notes,
        dietary_restrictions_other_notes=dietary_restrictions_other_notes,
        breakfast=breakfast,
        breakfast_notes=breakfast_notes,
        lunch=lunch,
        lunch_notes=lunch_notes,
        dinner=dinner,
        dinner_notes=dinner_notes,
        fresh_snacks=fresh_snacks,
        fresh_snacks_notes=fresh_snacks_notes,
        pantry_snacks=pantry_snacks,
        pantry_snacks_notes=pantry_snacks_notes,
        kids_meals=kids_meals,
        kids_allergies=kids_allergies,
        kids_meals_notes=kids_meals_notes,
        favorite_flowers=favorite_flowers,
    )

    return long_jet_preference


def update_long_jet_preferences(
    *,
    instance: LongJetPreferenceSheet,
    dietary_restrictions: str,
    dietary_restrictions_notes: str,
    dietary_restrictions_other_notes: str,
    breakfast: str,
    breakfast_notes: str,
    lunch: str,
    lunch_notes: str,
    dinner: str,
    dinner_notes: str,
    fresh_snacks: str,
    fresh_snacks_notes: str,
    pantry_snacks: str,
    pantry_snacks_notes: str,
    kids_meals: str,
    kids_allergies: str,
    kids_meals_notes: str,
    favorite_flowers: str,
) -> LongJetPreferenceSheet:
    """
    Updates Long Jet Preferences
    """

    instance.dietary_restrictions = dietary_restrictions
    instance.dietary_restrictions_notes = dietary_restrictions_notes
    instance.dietary_restrictions_other_notes = dietary_restrictions_other_notes
    instance.breakfast = breakfast
    instance.breakfast_notes = breakfast_notes
    instance.lunch = lunch
    instance.lunch_notes = lunch_notes
    instance.dinner = dinner
    instance.dinner_notes = dinner_notes
    instance.fresh_snacks = fresh_snacks
    instance.fresh_snacks_notes = fresh_snacks_notes
    instance.pantry_snacks = pantry_snacks
    instance.pantry_snacks_notes = pantry_snacks_notes
    instance.kids_meals = kids_meals
    instance.kids_allergies = kids_allergies
    instance.kids_meals_notes = kids_meals_notes
    instance.favorite_flowers = favorite_flowers

    instance.save()

    return instance
