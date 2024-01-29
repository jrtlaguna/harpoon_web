from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone

from core.models import Document


class GuestDetail(models.Model):
    """
    The guest of a charter
    """

    charters = models.ManyToManyField(
        "charter.Charter",
        related_name="guests",
        verbose_name="Trips",
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    emergency_contact = models.CharField(max_length=255)
    emergency_relation = models.CharField(max_length=255, blank=True, null=True)
    emergency_phone = models.CharField(max_length=255)
    address_street = models.CharField(max_length=255)
    address_number = models.CharField(max_length=255)
    address_city = models.CharField(max_length=255)
    nationality = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    passport_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    passport_expiration = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address_state = models.CharField(max_length=255)
    address_zipcode = models.CharField(max_length=255)
    address_country = models.CharField(max_length=255)
    medical_issues = models.TextField(null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    medications = models.TextField(null=True, blank=True)
    lactose_intolerant = models.BooleanField(default=False)
    shellfish_allergy = models.BooleanField(default=False)
    nut_allergy = models.BooleanField(default=False)
    gluten_free = models.BooleanField(default=False)
    none_food_sensitivity = models.BooleanField(default=False)
    other = models.BooleanField(default=False)
    other_notes = models.CharField(max_length=250, blank=True, null=True)
    salutation_nickname = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    high_priority_details = models.TextField(
        blank=True,
        null=True,
    )
    profile = models.OneToOneField(
        "guests.GuestProfile",
        on_delete=models.SET_NULL,
        related_name="details",
        null=True,
        blank=True,
    )
    passport = models.FileField(
        verbose_name="Passport",
        blank=True,
        null=True,
    )

    @property
    def documents(self):
        return Document.objects.filter(
            model_id=self.id, model=Document.ModelChoices.GUEST_DETAIL
        )

    @property
    def is_principal(self):
        return self.principal_charters.exists()

    @property
    def has_food_pref(self):
        return hasattr(self, "food_preferences") and self.food_preferences is not None

    @property
    def has_meal_and_room_pref(self):
        return (
            hasattr(self, "meal_and_room_preferences")
            and self.meal_and_room_preferences is not None
        )

    @property
    def has_diet_services_sizes_pref(self):
        return (
            hasattr(self, "diet_services_sizes_preferences")
            and self.diet_services_sizes_preferences is not None
        )

    @property
    def has_beverages_and_alcoholic_pref(self):
        return (
            hasattr(self, "beverages_and_alcoholic_preferences")
            and self.beverages_and_alcoholic_preferences is not None
        )

    @property
    def long_jet_complete(self):
        return (
            hasattr(self, "long_jet_preference")
            and self.long_jet_preference is not None
        )

    @property
    def short_jet_complete(self):
        return (
            hasattr(self, "short_jet_preference")
            and self.short_jet_preference is not None
        )

    @property
    def is_incomplete(self):
        properties = [
            "has_food_pref",
            "has_meal_and_room_pref",
            "has_diet_services_sizes_pref",
            "has_beverages_and_alcoholic_pref",
        ]
        charter_fields = [
            "emergency_contact",
            "emergency_phone",
            "address_street",
            "address_number",
            "address_city",
            "address_state",
            "address_zipcode",
            "address_country",
            "medical_issues",
            "allergies",
            "medications",
            "profile",
        ]
        return any(
            getattr(self, field) is False
            for field in [
                *properties,
                *charter_fields,
            ]
        )

    @property
    def notification_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ({self.email})"
        return self.email

    @property
    def proper_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.email

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.email

    @property
    def food_sensitivities(self) -> list[str]:
        allergies = []
        if self.none_food_sensitivity is True:
            return []

        allergy_fields = [
            "lactose_intolerant",
            "shellfish_allergy",
            "nut_allergy",
            "gluten_free",
        ]
        for allergy in allergy_fields:
            if getattr(self, allergy) is True:
                allergies.append(allergy.replace("_", " ").title())

        if self.other and self.other_notes not in [None, ""]:
            allergies.append(self.other_notes)

        return allergies

    @property
    def has_dietary_restrictions(self):
        dietary_restrictions = False
        food_sensitivities = self.food_sensitivities not in ["", None, []]
        if hasattr(self, "meal_and_room_preferences"):
            dietary_restrictions = (
                getattr(self.meal_and_room_preferences, "dietary_restrictions")
                not in [None, ""]
                or getattr(
                    self.meal_and_room_preferences, "dietary_restrictions_other_notes"
                )
                not in [None, ""]
                or getattr(self.meal_and_room_preferences, "dietary_restrictions_notes")
                not in [None, ""]
            )
        return any([dietary_restrictions, food_sensitivities])

    def save(self, *args, **kwargs):
        allergy_fields = [
            "lactose_intolerant",
            "shellfish_allergy",
            "nut_allergy",
            "gluten_free",
            "other",
        ]

        if not self.other:
            self.other_notes = ""

        if any(getattr(self, field) is True for field in allergy_fields):
            self.none_food_sensitivity = False

        return super(GuestDetail, self).save(*args, **kwargs)

    def completed_preference(self):
        return (
            hasattr(self, "short_jet_preference")
            and hasattr(self, "long_jet_preference")
            and hasattr(self, "food_preferences")
        )

    class Meta:
        verbose_name = "Guest Detail"
        verbose_name_plural = "Guest Details"


class Charter(models.Model):
    """
    Represents a charter trip
    """

    class Meta:
        verbose_name = "Charter"
        verbose_name_plural = "Charters"

    created_by = models.ForeignKey(
        "authentication.User",
        related_name="created_charters",
        verbose_name="Created By",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    vessel = models.ForeignKey(
        "vessels.Vessel",
        related_name="charters",
        verbose_name="Vessel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    principal_guest = models.ForeignKey(
        "charter.GuestDetail",
        related_name="principal_charters",
        verbose_name="Principal Guest",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    apa_budget = models.FloatField()
    currency = models.CharField(max_length=10, blank=True, null=True)
    embark_location = models.CharField(max_length=255, blank=True, null=True)
    embark_date = models.DateField()
    embark_time = models.CharField(max_length=255, blank=True, null=True)
    embark_name_of_dock = models.CharField(max_length=255, blank=True, null=True)
    embark_city = models.CharField(max_length=255, blank=True, null=True)
    embark_country = models.CharField(max_length=255, blank=True, null=True)
    embark_additional_info = models.TextField(blank=True, null=True)
    disembark_location = models.CharField(max_length=255, blank=True, null=True)
    disembark_date = models.DateField()
    disembark_time = models.CharField(max_length=255, blank=True, null=True)
    disembark_city = models.CharField(max_length=255, blank=True, null=True)
    disembark_name_of_dock = models.CharField(max_length=255, blank=True, null=True)
    disembark_country = models.CharField(max_length=255, blank=True, null=True)
    disembark_additional_info = models.TextField(blank=True, null=True)
    booking_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        if self.principal_guest:
            return (
                f"{self.principal_guest.last_name} {self.embark_date.strftime('%b %Y')}"
            )
        else:
            return f"{self.embark_date.strftime('%b %Y')}"

    @property
    def principle_guest(self):
        return f"{str(self.guests.filter(is_principal=True).first()) or ''}"

    @property
    def is_active(self):
        return self.embark_date <= timezone.now().date() <= self.disembark_date

    @property
    def is_upcoming(self):
        return self.embark_date > timezone.now().date()

    @property
    def is_past_due(self):
        return self.disembark_date < timezone.now().date()

    @property
    def incomplete_unregistered_guests(self):
        guests = self.guests.exclude(id=self.principal_guest.id)
        guest_object_list = [guest for guest in guests if guest.is_incomplete]
        return [guest.notification_name for guest in guest_object_list]

    @property
    def complete_registered_guests(self):
        guests = self.guests.exclude(id=self.principal_guest.id)
        guest_object_list = [guest for guest in guests if not guest.is_incomplete]
        return [guest.notification_name for guest in guest_object_list]


class FoodPreferences(models.Model):
    """
    Represents the food preferences of a specific guest.
    """

    class Meta:
        verbose_name = "Food Preference"
        verbose_name_plural = "Food Preferences"

    class GeneralCuisine(models.TextChoices):
        AMERICAN = ("AMERICAN", "American")
        BRITISH = ("BRITISH", "British")
        CHINESE = ("CHINESE", "Chinese")
        FRENCH = ("FRENCH", "French")
        FUSION = ("FUSION", "Fusion")
        INDIAN = ("INDIAN", "Indian")
        ITALIAN = ("ITALIAN", "Italian")
        JAPANESE = ("JAPANESE", "Japanese")
        MEXICAN = ("MEXICAN", "Mexican")
        NORTH_AMERICAN = ("NORTH_AMERICAN", "North American")
        SPANISH = ("SPANISH", "Spanish")
        THAI = ("THAI", "Thai")
        NONE = ("NONE", "None")

    class FishAndShellfish(models.TextChoices):
        CRAB = ("CRAB", "Crab")
        LOBSTER = ("LOBSTER", "Lobster")
        CONCH = ("CONCH", "Conch")
        CLAMS = ("CLAMS", "Clams")
        MUSSELS = ("MUSSELS", "Mussels")
        OYSTER = ("OYSTER", "Oyster")
        SCALLOPS = ("SCALLOPS", "Scallops")
        ESCARGOT = ("ESCARGOT", "Escargot")
        SQUID_CALAMARI = ("SQUID_CALAMARI", "Squid / Calamari")
        OCTOPUS = ("OCTOPUS", "Octopus")
        SMOKED_SALMON = ("SMOKED_SALMON", "Smoked Salmon")
        COD = ("COD", "Cod")
        MAHI = ("MAHI", "Mahi")
        TROUT = ("TROUT", "Trout")
        SARDINES = ("SARDINES", "Sardines")
        NONE = ("NONE", "None")

    class Meat(models.TextChoices):
        BEEF = ("BEEF", "Beef")
        CHICKEN = ("CHICKEN", "Chicken")
        DUCK = ("DUCK", "Duck")
        LAMB = ("LAMB", "Lamb")
        PORK = ("PORK", "Pork")
        TURKEY = ("TURKEY", "Turkey")
        VEAL = ("VEAL", "Veal")
        NONE = ("NONE", "None")

    class Bread(models.TextChoices):
        BAGEL = ("BAGEL", "Bagel")
        BAGUETTE = ("BAGUETTE", "Baguette")
        RYE = ("RYE", "Rye")
        BREADSTICKS = ("BREADSTICKS", "Breadsticks")
        BRIOCHÉ = ("BRIOCHÉ", "Brioché")
        BROWN = ("BROWN", "Brown")
        CIABATTA = ("CIABATTA", "Ciabatta")
        FOCACCIA = ("FOCACCIA", "Focaccia")
        PITA = ("PITA", "Pita")
        WHITE = ("WHITE", "White")
        NONE = ("NONE", "None")

    class Soup(models.TextChoices):
        BORSCHT = ("BORSCHT", "Borscht")
        BOUILLABAISSE = ("BOUILLABAISSE", "Bouillabaisse")
        CONSOMMÉ = ("CONSOMMÉ", "Consommé")
        CREAMED_VELOUTÉ = ("CREAMED_VELOUTÉ", "Creamed / Velouté")
        FRUIT = ("FRUIT", "Fruit")
        FRENCH_ONION = ("FRENCH_ONION", "French Onion")
        GAZPACHO = ("GAZPACHO", "Gazpacho")
        LOBSTER_BISQUE = ("LOBSTER_BISQUE", "Lobster Bisque")
        MINESTRONE = ("MINESTRONE", "Minestrone")
        MISO = ("MISO", "Miso")
        TOMATO = ("TOMATO", "Tomato")
        VEGETABLE_BROTH = ("VEGETABLE_BROTH", "Vegetable Broth")
        VICHYSSOISE = ("VICHYSSOISE", "Vichyssoise")
        NONE = ("NONE", "None")

    class Salad(models.TextChoices):
        CAPRESE = ("CAPRESE", "Caprese")
        CAESAR = ("CAESAR", "Caesar")
        COLESLAW = ("COLESLAW", "Coleslaw")
        GREEK = ("GREEK", "Greek")
        BRIOCHE = ("BRIOCHE", "Brioche")
        MIXED_LEAF = ("MIXED_LEAF", "Mixed Leaf")
        NICOISE = ("NICOISE", "Nicoise")
        PASTA = ("PASTA", "Pasta")
        POTATO = ("POTATO", "Potato")
        RUSSIAN = ("RUSSIAN", "Russian")
        SEAFOOD = ("SEAFOOD", "Seafood")
        NONE = ("NONE", "None")

    class Cheese(models.TextChoices):
        BLUE = ("BLUE", "Blue")
        BRIE = ("BRIE", "Brie")
        GOUDA = ("GOUDA", "Gouda")
        CHEDDAR = ("CHEDDAR", "Cheddar")
        FETA = ("FETA", "Feta")
        PARMESAN = ("PARMESAN", "Parmesan")
        GOAT = ("GOAT", "Goat")
        CAMEMBERT = ("CAMEMBERT", "Camembert")
        MOZZARELLA = ("MOZZARELLA", "Mozzarella")
        VEGAN = ("VEGAN", "Vegan")
        NONE = ("NONE", "None")

    class Dessert(models.TextChoices):
        CHOCOLATE = ("CHOCOLATE", "Chocolate")
        CARAMEL = ("CARAMEL", "Caramel")
        CREAMY = ("CREAMY", "Creamy")
        CAKE = ("CAKE", "Cake")
        FRUIT_SALAD = ("FRUIT_SALAD", "Fruit Salad")
        ICE_CREAM = ("ICE_CREAM", "Ice Cream")
        MOUSSE = ("MOUSSE", "Mousse")
        SORBETS = ("SORBETS", "Sorbets")
        SOUFFLÉS = ("SOUFFLÉS", "Soufflés")
        TARTS = ("TARTS", "Tarts")
        LIGHT = ("LIGHT", "Light")
        NONE = ("NONE", "None")

    guest = models.OneToOneField(
        "charter.GuestDetail", related_name="food_preferences", on_delete=models.CASCADE
    )
    general_cuisine = models.CharField(max_length=255)
    general_cuisine_notes = models.TextField(null=True, blank=True)
    fish_and_shellfish = models.CharField(max_length=255)
    fish_and_shellfish_notes = models.TextField(null=True, blank=True)
    meat = models.CharField(max_length=255)
    meat_notes = models.TextField(null=True, blank=True)
    bread = models.CharField(max_length=255)
    bread_notes = models.TextField(null=True, blank=True)
    salad = models.CharField(max_length=255)
    salad_notes = models.TextField(null=True, blank=True)
    soup = models.CharField(max_length=255)
    soup_notes = models.TextField(null=True, blank=True)
    cheese = models.CharField(max_length=255)
    cheese_notes = models.TextField(null=True, blank=True)
    dessert = models.CharField(max_length=255)
    dessert_notes = models.TextField(null=True, blank=True)
    kids_allergies = models.CharField(
        verbose_name="Kids Allergies",
        max_length=250,
        blank=True,
        null=True,
    )
    kids_meals = models.CharField(
        verbose_name="Kids Meals",
        max_length=250,
        blank=True,
        null=True,
    )
    kids_meals_notes = models.CharField(
        verbose_name="Kids Meals Notes",
        max_length=250,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    @property
    def is_complete(self):
        required_fields = [
            "general_cuisine",
            "fish_and_shellfish",
            "meat",
            "bread",
            "salad",
            "soup",
            "cheese",
            "dessert",
        ]
        return all(getattr(self, field) is not None for field in required_fields)

    def __str__(self):
        return f"{self.guest.first_name} {self.guest.last_name}"


class MealAndRoomPreferences(models.Model):
    """
    Represents the meal and room preferences of a specific guest.
    """

    class Meta:
        verbose_name = "Meal and Room Preference"
        verbose_name_plural = "Meal and Room Preferences"

    _24_range = range(0, 24)

    time_range = [str(e) for e in range(0, 24)]
    time_choices = []
    for time in time_range:
        time_choices += [
            (f"_{time.zfill(2)}00", f"{time.zfill(2)}:00"),
            (f"_{time.zfill(2)}30", f"{time.zfill(2)}:30"),
        ]

    class CanapesTime(models.TextChoices):
        BEFORE_LUNCH = ("BEFORE_LUNCH", "Before Lunch")
        BEFORE_DINNER = ("BEFORE_DINNER", "Before Dinner")

    class CanapesTypes(models.TextChoices):
        LIGHT = ("LIGHT", "Light")
        FULL_SELECTION = ("FULL_SELECTION", "Full Selection")
        NONE = ("NONE", "None")

    class MidMorningSnacks(models.TextChoices):
        SWEET = ("SWEET", "Sweet")
        SAVORY = ("SAVORY", "Savory")
        NONE = ("NONE", "None")

    class MidAfternoonSnacks(models.TextChoices):
        SWEET = ("SWEET", "Sweet")
        SAVORY = ("SAVORY", "Savory")
        NONE = ("NONE", "None")

    class DietaryRestrictions(models.TextChoices):
        VEGAN = ("VEGAN", "Vegan")
        VEGETARIAN = ("VEGETARIAN", "Vegetarian")
        PALEO = ("PALEO", "Paleo")
        PESCATARIAN = ("PESCATARIAN", "Pescatarian")
        NONE = ("NONE", "None")

    guest = models.OneToOneField(
        "charter.GuestDetail",
        related_name="meal_and_room_preferences",
        on_delete=models.CASCADE,
    )
    dietary_restrictions = models.CharField(
        max_length=225, choices=DietaryRestrictions.choices, null=True, blank=True
    )
    dietary_restrictions_other_notes = models.CharField(
        max_length=255, null=True, blank=True
    )
    dietary_restrictions_notes = models.TextField(null=True)
    breakfast_time = models.CharField(max_length=255, choices=time_choices)
    breakfast_note = models.TextField()
    lunch_time = models.CharField(max_length=255, choices=time_choices)
    lunch_note = models.TextField()
    dinner_time = models.CharField(max_length=255, choices=time_choices)
    dinner_note = models.TextField()
    canapes_time = models.CharField(max_length=255, choices=CanapesTime.choices)
    canapes_selection = models.CharField(max_length=255, choices=CanapesTypes.choices)
    midmorning_snacks = models.CharField(
        max_length=255, choices=MidMorningSnacks.choices
    )
    midafternoon_snacks = models.CharField(
        max_length=255, choices=MidAfternoonSnacks.choices
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    @property
    def is_complete(self):
        required_fields = [
            "breakfast_time",
            "lunch_time",
            "dinner_time",
            "canapes_time",
            "canapes_selection",
            "midmorning_snacks",
            "midafternoon_snacks",
            "breakfast_selection",
            "lunch_selection",
            "dinner_selection",
        ]
        return all(getattr(self, field) is not None for field in required_fields)

    def __str__(self):
        return f"{self.guest.first_name} {self.guest.last_name}"


class BreakfastSelection(models.Model):
    """
    Represents a breakfast option.
    """

    class BreakfastSelection(models.TextChoices):
        BUFFET = ("BUFFET", "Buffet")
        ROOM_SERVICE = ("ROOM_SERVICE", "Room Service")
        TABLE_SERVICE = ("TABLE_SERVICE", "Table Service")
        ALFRESCO = ("ALFRESCO", "Alfresco (Outdoors)")
        FAMILY_STYLE = ("FAMILY_STYLE", "Family Style")
        CHEFS_CHOICE = ("CHEFS_CHOICE", "Chef's Choice")

    meal_and_room_preference = models.OneToOneField(
        "charter.MealAndRoomPreferences",
        related_name="breakfast_selection",
        verbose_name="Meal And Room Preference",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=255)

    @property
    def is_complete(self):
        return bool(self.name)

    def __str__(self):
        return (
            str(self.meal_and_room_preference)
            if self.meal_and_room_preference
            else "Untitled Meal and Room Preference"
        )

    class Meta:
        verbose_name = "Breakfast Selection"
        verbose_name_plural = "Breakfast Selections"


class LunchSelection(models.Model):
    """
    Represents a lunch option.
    """

    class LunchSelection(models.TextChoices):
        BUFFET = ("BUFFET", "Buffet")
        RUSSIAN_STYLE = ("RUSSIAN_STYLE", "Russian Style")
        _2_COURSE = ("_2_COURSE", "2-Course")
        BBQ = ("BBQ", "BBQ")
        _3_COURSE = ("_3_COURSE", "3-Course")
        INFORMAL = ("INFORMAL", "Informal")
        _4_COURSE = ("_4_COURSE", "4-Course")
        FORMAL = ("FORMAL", "Formal")
        FAMILY_STYLE = ("FAMILY_STYLE", "Family Style")
        LIGHT = ("LIGHT", "Light")
        CHEF_TASTING_MENU_STYLE = (
            "CHEF_TASTING_MENU_STYLE",
            "Chef's Tasting Menu Style",
        )

    meal_and_room_preference = models.OneToOneField(
        "charter.MealAndRoomPreferences",
        related_name="lunch_selection",
        verbose_name="Meal And Room Preference",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=255)

    @property
    def is_complete(self):
        required_fields = [
            "name",
        ]
        return all(getattr(self, field) is not None for field in required_fields)

    def __str__(self):
        return (
            str(self.meal_and_room_preference)
            if self.meal_and_room_preference
            else "Untitled Meal and Room Preference"
        )

    class Meta:
        verbose_name = "Lunch Selection"
        verbose_name_plural = "Lunch Selections"


class DinnerSelection(models.Model):
    """
    Represents a dinner option.
    """

    class DinnerSelection(models.TextChoices):
        BUFFET = ("BUFFET", "Buffet")
        RUSSIAN_STYLE = ("RUSSIAN_STYLE", "Russian Style")
        _2_COURSE = ("_2_COURSE", "2-Course")
        BBQ = ("BBQ", "BBQ")
        _3_COURSE = ("_3_COURSE", "3-Course")
        INFORMAL = ("INFORMAL", "Informal")
        _4_COURSE = ("_4_COURSE", "4-Course")
        FORMAL = ("FORMAL", "Formal")
        FAMILY_STYLE = ("FAMILY_STYLE", "Family Style")
        LIGHT = ("LIGHT", "Light")
        CHEF_TASTING_MENU_STYLE = (
            "CHEF_TASTING_MENU_STYLE",
            "Chef's Tasting Menu Style",
        )

    meal_and_room_preference = models.OneToOneField(
        "charter.MealAndRoomPreferences",
        related_name="dinner_selection",
        verbose_name="Meal And Room Preference",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=255)

    @property
    def is_complete(self):
        required_fields = [
            "name",
        ]
        return all(getattr(self, field) is not None for field in required_fields)

    def __str__(self):
        return (
            str(self.meal_and_room_preference)
            if self.meal_and_room_preference
            else "Untitled Meal and Room Preference"
        )

    class Meta:
        verbose_name = "Dinner Selection"
        verbose_name_plural = "Dinner Selections"


class DietServicesSizesPreferences(models.Model):
    """
    Represents the diet, services, and size preferences of a guest.
    """

    class Meta:
        verbose_name = "Diet, Services & Sizes Preference"
        verbose_name_plural = "Diet, Services & Sizes Preferences"

    class OtherServices(models.TextChoices):
        MASSAGE_THERAPY = ("MASSAGE_THERAPY", "Massage Therapy")
        YOGA_INSTRUCTION = ("YOGA_INSTRUCTION", "Yoga Instruction")
        DIVING_EXCURSION = ("DIVING_EXCURSION", "Diving Excursion")
        LAND_EXCURSION = ("LAND_EXCURSION", "Land Excursion")

    class ShirtSizing(models.TextChoices):
        MENS = ("MENS", "Men's")
        WOMENS = ("WOMENS", "Women's")

    class InternationalShirtSizing(models.TextChoices):
        US = ("US", "US")
        UK = ("UK", "UK")
        EU = ("EU", "EU")

    class ShirtSizes(models.TextChoices):
        XS = ("XS", "Extra Small")
        L = ("L", "Large")
        S = ("S", "Small")
        XL = ("XL", "Extra Large")
        M = ("M", "Medium")

    class ShoeSizing(models.TextChoices):
        MENS = ("MENS", "Men's")
        WOMENS = ("WOMENS", "Women's")

    class InternationalShoeSizing(models.TextChoices):
        US = ("US", "US")
        UK = ("UK", "UK")
        EU = ("EU", "EU")

    guest = models.OneToOneField(
        "charter.GuestDetail",
        related_name="diet_services_sizes_preferences",
        on_delete=models.CASCADE,
    )
    preferred_room_temperature = models.CharField(max_length=225, null=True)
    favorite_flowers = models.CharField(max_length=255, null=True)
    other_services_other_notes = models.CharField(max_length=255, null=True, blank=True)
    shirt_sizing = models.CharField(max_length=225, choices=ShirtSizing.choices)
    international_shirt_sizing = models.CharField(
        max_length=225, choices=InternationalShirtSizing.choices
    )
    shirt_size = models.CharField(max_length=225, choices=ShirtSizes.choices)
    shoe_sizing = models.CharField(max_length=225, choices=ShoeSizing.choices)
    international_shoe_sizing = models.CharField(
        max_length=225, choices=InternationalShoeSizing.choices
    )
    shoe_size = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    @property
    def is_complete(self):
        required_fields = [
            "dietary_restrictions",
            "preferred_room_temperature",
            "favorite_flowers",
            "shirt_sizing",
            "international_shirt_sizing",
            "shirt_size",
            "shoe_sizing",
            "international_shoe_sizing",
            "shoe_size",
        ]

        return all(getattr(self, field) is not None for field in required_fields)

    def __str__(self):
        return f"{self.guest.first_name} {self.guest.last_name}"


class OtherServices(models.Model):
    """
    Other room services that the guest might need.
    """

    diet_services_sizes_preferences = models.OneToOneField(
        "charter.DietServicesSizesPreferences",
        related_name="other_service",
        verbose_name="Diet Services Sizes Preferences",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=225)

    @property
    def is_complete(self):
        required_fields = [
            "name",
        ]
        return all(getattr(self, field) is not None for field in required_fields)

    def __str__(self):
        return (
            str(self.diet_services_sizes_preferences)
            if self.diet_services_sizes_preferences
            else "Untitled Preference"
        )

    class Meta:
        verbose_name = "Other Service"
        verbose_name_plural = "Other Services"


class BeveragesAndAlcoholicPreferences(models.Model):
    """
    Represents the beverage and alcoholic preference of the guest.
    """

    class MilkSelections(models.TextChoices):
        WHOLE = ("WHOLE", "Whole")
        ALMOND = ("ALMOND", "Almond")
        OAT = ("OAT", "Oat")
        SOYA = ("SOY", "Soy")
        _2PCT_MILK = ("_2PCT_MILK", "2% Milk")
        RICE = ("RICE", "Rice")
        SKIM = ("SKIM", "Skim")
        NONE = ("NONE", "None")

    class CoffeeSelections(models.TextChoices):
        CAPPUCCINO = ("CAPPUCCINO", "Cappuccino")
        ESPRESSO = ("ESPRESSO", "Espresso")
        LATTE = ("LATTE", "Latte")
        MACIADO = ("MACIADO", "Macchiato")
        AMERICAN = ("AMERICAN", "American")
        ICED_COFFEE = ("ICED_COFFEE", "Iced Coffee")
        NONE = ("NONE", "None")

    class TeaSelections(models.TextChoices):
        EARL_GREY = ("EARL_GREY", "Earl Grey")
        HERBAL_TEA = ("HERBAL_TEA", "Herbal Tea")
        ROOIBOS = ("ROOIBOS", "Rooibos")
        CHAMOMILLE = ("CHAMOMILLE", "Chamomile")
        MINT = ("MINT", "Mint")
        GREEN_TEA = ("GREEN_TEA", "Green Tea")
        NONE = ("NONE", "None")

    class WaterSelections(models.TextChoices):
        SPARKLING = ("SPARKLING", "Sparkling")
        BOTTLED = ("BOTTLED", "Bottled Water")
        STILL = ("STILL", "Still")
        NONE = ("NONE", "None")

    class JuiceSelections(models.TextChoices):
        GRAPE_FRUIT = ("GRAPE_FRUIT", "Grapefruit")
        APPLE = ("APPLE", "Apple")
        ORANGE = ("ORANGE", "Orange")
        CARROT = ("CARROT", "Carrot")
        FRESH_PINEAPPLE = ("FRESH_PINEAPPLE", "Fresh Pineapple")
        GREEN_JUICE = ("GREEN_JUICE", "Green Juice")
        NONE = ("NONE", "None")

    class SodasMixersSelections(models.TextChoices):
        COKE = ("COKE", "Coke")
        TONIC = ("TONIC", "Tonic")
        DC = ("DC", "DC")
        LA_CROIX = ("LA_CROIX", "La Croix")
        PEPSI = ("PEPSI", "Pepsi")
        RED_BULL = ("RED_BULL", "Red Bull")
        GINGER_ALE = ("GINGER_ALE", "Ginger Ale")
        _7_UP = ("_7_UP", "7 Up")
        SODA_WATER = ("SODA_WATER", "Soda Water")
        SPRITE = ("SPRITE", "Sprite")
        NONE = ("NONE", "None")

    class AddOnsSelections(models.TextChoices):
        CITRUS = ("CITRUS", "Citrus")
        CREAMER = ("CREAMER", "Creamer")
        SWEETENER = ("SWEETENER", "Sweetener")
        SUGAR = ("SUGAR", "Sugar")
        NONE = ("NONE", "None")

    guest = models.OneToOneField(
        "charter.GuestDetail",
        related_name="beverages_and_alcoholic_preferences",
        on_delete=models.CASCADE,
    )
    milk_note = models.TextField()
    coffee_note = models.TextField()
    tea_note = models.TextField()
    water_note = models.TextField()
    juice_note = models.TextField()
    sodas_and_mixers_note = models.TextField()
    add_ons_note = models.TextField()
    whiskey_name = models.CharField(max_length=255, null=True, blank=True)
    whiskey_quantity = models.IntegerField(default=0)
    extra_whiskey = models.JSONField(null=True, blank=True)
    brandy_name = models.CharField(max_length=255, null=True, blank=True)
    brandy_quantity = models.IntegerField(default=0)
    extra_brandy = models.JSONField(null=True, blank=True)
    vodka_name = models.CharField(max_length=255, null=True, blank=True)
    vodka_quantity = models.IntegerField(default=0)
    extra_vodka = models.JSONField(null=True, blank=True)
    tequila_name = models.CharField(max_length=255, null=True, blank=True)
    tequila_quantity = models.IntegerField(default=0)
    extra_tequila = models.JSONField(null=True, blank=True)
    rum_name = models.CharField(max_length=255, null=True, blank=True)
    rum_quantity = models.IntegerField(default=0)
    extra_rum = models.JSONField(null=True, blank=True)
    liquors_name = models.CharField(max_length=255, null=True, blank=True)
    liquors_quantity = models.IntegerField(default=0)
    extra_liquors = models.JSONField(null=True, blank=True)
    cocktail_name = models.CharField(max_length=255, null=True, blank=True)
    cocktail_quantity = models.IntegerField(default=0)
    extra_cocktail = models.JSONField(null=True, blank=True)
    port_beer_name = models.CharField(max_length=255, null=True, blank=True)
    port_beer_quantity = models.IntegerField(default=0)
    extra_port_beer = models.JSONField(null=True, blank=True)
    red_wine_name = models.CharField(max_length=255, null=True, blank=True)
    red_wine_quantity = models.IntegerField(default=0)
    extra_red_wine = models.JSONField(null=True, blank=True)
    white_wine_name = models.CharField(max_length=255, null=True, blank=True)
    white_wine_quantity = models.IntegerField(default=0)
    extra_white_wine = models.JSONField(null=True, blank=True)
    rose_wine_name = models.CharField(max_length=255, null=True, blank=True)
    rose_wine_quantity = models.IntegerField(default=0)
    extra_rose_wine = models.JSONField(null=True, blank=True)
    champagne_name = models.CharField(max_length=255, null=True, blank=True)
    champagne_quantity = models.IntegerField(default=0)
    extra_champagne = models.JSONField(null=True, blank=True)
    other_name = models.CharField(max_length=255, null=True, blank=True)
    other_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    @property
    def is_complete(self):
        required_fields = [
            "milk_note",
            "coffee_note",
            "tea_note",
            "water_note",
            "juice_note",
            "sodas_and_mixers_note",
            "add_ons_note",
            "whiskey_name",
            "whiskey_quantity",
            "brandy_name",
            "brandy_quantity",
            "vodka_name",
            "vodka_quantity",
            "tequila_name",
            "tequila_quantity",
            "rum_name",
            "rum_quantity",
            "liquors_name",
            "liquors_quantity",
            "cocktail_name",
            "cocktail_quantity",
            "port_beer_name",
            "port_beer_quantity",
            "red_wine_name",
            "red_wine_quantity",
            "white_wine_name",
            "white_wine_quantity",
            "champagne_name",
            "champagne_quantity",
            "other_name",
            "other_quantity",
            "milk_selections",
            "coffee_selections",
            "tea_selections",
            "water_selections",
            "juice_selections",
            "sodas_and_mixers_selections",
            "add_ons_selections",
        ]

        return all(getattr(self, field) is not None for field in required_fields)

    def __str__(self):
        return (
            f"{self.guest.first_name} {self.guest.last_name}"
            if self.guest
            else "Untitled Preference"
        )

    class Meta:
        verbose_name = "Beverages and Preferences"
        verbose_name_plural = "Beverages and Preferences"


class MilkSelection(models.Model):
    beverages_and_alcoholic_preferences = models.OneToOneField(
        "charter.BeveragesAndAlcoholicPreferences",
        related_name="milk_selection",
        verbose_name="Beverages And Alcoholic Preferences",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=225)

    def __str__(self):
        return (
            str(self.beverages_and_alcoholic_preferences)
            if self.beverages_and_alcoholic_preferences
            else "Untitled Beverages Preference"
        )


class CoffeeSelection(models.Model):
    beverages_and_alcoholic_preferences = models.OneToOneField(
        "charter.BeveragesAndAlcoholicPreferences",
        related_name="coffee_selection",
        verbose_name="Beverages And Alcoholic Preferences",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=225)

    def __str__(self):
        return (
            str(self.beverages_and_alcoholic_preferences)
            if self.beverages_and_alcoholic_preferences
            else "Untitled Beverages Preference"
        )

    class Meta:
        verbose_name = "Coffee Selection"
        verbose_name_plural = "Coffee Selections"


class TeaSelection(models.Model):
    beverages_and_alcoholic_preferences = models.OneToOneField(
        "charter.BeveragesAndAlcoholicPreferences",
        related_name="tea_selection",
        verbose_name="Beverages And Alcoholic Preferences",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=225)

    def __str__(self):
        return (
            str(self.beverages_and_alcoholic_preferences)
            if self.beverages_and_alcoholic_preferences
            else "Untitled Beverages Preference"
        )

    class Meta:
        verbose_name = "Tea Selection"
        verbose_name_plural = "Tea Selections"


class WaterSelection(models.Model):
    beverages_and_alcoholic_preferences = models.OneToOneField(
        "charter.BeveragesAndAlcoholicPreferences",
        related_name="water_selection",
        verbose_name="Beverages And Alcoholic Preferences",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=225)

    def __str__(self):

        return (
            str(self.beverages_and_alcoholic_preferences)
            if self.beverages_and_alcoholic_preferences
            else "Untitled Beverages Preference"
        )

    class Meta:
        verbose_name = "Water Selection"
        verbose_name_plural = "Water Selections"


class JuiceSelection(models.Model):
    beverages_and_alcoholic_preferences = models.OneToOneField(
        "charter.BeveragesAndAlcoholicPreferences",
        related_name="juice_selection",
        verbose_name="Beverages And Alcoholic Preferences",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=225)

    def __str__(self):
        return (
            str(self.beverages_and_alcoholic_preferences)
            if self.beverages_and_alcoholic_preferences
            else "Untitled Beverages Preference"
        )

    class Meta:
        verbose_name = "Juice Selection"
        verbose_name_plural = "Juice Selections"


class SodasAndMixersSelection(models.Model):
    beverages_and_alcoholic_preferences = models.OneToOneField(
        "charter.BeveragesAndAlcoholicPreferences",
        related_name="sodas_and_mixers_selection",
        verbose_name="Beverages And Alcoholic Preferences",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=225)

    def __str__(self):
        return (
            str(self.beverages_and_alcoholic_preferences)
            if self.beverages_and_alcoholic_preferences
            else "Untitled Beverages Preference"
        )

    class Meta:
        verbose_name = "Sodas and Mixers Selection"
        verbose_name_plural = "Sodas and Mixers Selections"


class AddOnsSelection(models.Model):
    beverages_and_alcoholic_preferences = models.OneToOneField(
        "charter.BeveragesAndAlcoholicPreferences",
        related_name="add_ons_selection",
        verbose_name="Beverages And Alcoholic Preferences",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=225)

    def __str__(self):
        return (
            str(self.beverages_and_alcoholic_preferences)
            if self.beverages_and_alcoholic_preferences
            else "Untitled Beverages Preference"
        )
