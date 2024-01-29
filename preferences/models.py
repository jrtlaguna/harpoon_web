from django.db import models


class DietaryRestrictionChoices(models.TextChoices):
    VEGAN = ("VEGAN", "Vegan")
    PALEO = ("PALEO", "Paleo")
    VEGETARIAN = ("VEGETARIAN", "Vegetarian")
    PESCETARIAN = ("PESCETARIAN", "Pescetarian")
    GLUTEN_FREE = ("GLUTEN_FREE", "Gluten Free")
    NONE = ("NONE", "None")
    OTHER = ("OTHER", "Other")


class KidsChoices(models.TextChoices):
    FISH = ("FISH", "Fish")
    STEAMED_VEGGIES = ("STEAMED_VEGGIES", "Steamed Veggies")
    CHICKEN = ("CHICKEN", "Chicken")
    PIZZA = ("PIZZA", "Pizza")
    BEEF = ("BEEF", "Beef")
    SNACKS = ("SNACKS", "Snacks")
    PASTA = ("PASTA", "Pasta")
    VEGETARIAN = ("VEGETARIAN", "Vegetarian")
    RICE = ("RICE", "Rice")
    NONE = ("NONE", "None")


class ShortJetPreferenceSheet(models.Model):
    class BreakfastChoices(models.TextChoices):
        EGG_SANDIWCH = ("EGG_SANDIWCH", "Egg Sandiwch")
        LIGHT = ("LIGHT", "Light")
        YOGURT = ("YOGURT", "Yogurt")
        DOUGHNUTS = ("DOUGHNUTS", "Doughnuts")
        MUFFINS = ("MUFFINS", "Muffins")
        NONE = ("NONE", "None")

    class LunchChoices(models.TextChoices):
        FRUIT_PLATTER = ("FRUIT_PLATTER", "Fruit Platter")
        MIXED_SALAD = ("MIXED_SALAD", "Mixed Salad")
        VEGGIE_PLATTER = ("VEGGIE_PLATTER", "Veggie Platter")
        SANDWICH = ("SANDWICH", "Sandwich (Specify below)")
        WRAP = ("WRAP", "Wrap (Specify below)")
        NONE = ("NONE", "None")
        SUSHI = ("SUSHI", "Sushi")

    class DinnerChoices(models.TextChoices):
        BEEF = ("BEEF", "Beef")
        FISH = ("FISH", "Fish")
        VEGETARIAN = ("VEGETARIAN", "Vegetarian")
        CHICKEN = ("CHICKEN", "Chicken")
        NONE = ("NONE", "None")

    guest = models.OneToOneField(
        "charter.GuestDetail",
        verbose_name="Guest",
        related_name="short_jet_preference",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    dietary_restrictions = models.CharField(
        verbose_name="Dietary Restrictions",
        choices=DietaryRestrictionChoices.choices,
        max_length=50,
        null=True,
        blank=True,
    )
    dietary_restrictions_notes = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    dietary_restrictions_other_notes = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    breakfast = models.CharField(
        verbose_name="Breakfast",
        max_length=250,
        blank=True,
        null=True,
    )
    breakfast_notes = models.CharField(
        verbose_name="Breakfast Notes",
        max_length=250,
        blank=True,
        null=True,
    )
    lunch = models.CharField(
        verbose_name="Lunch",
        max_length=250,
        blank=True,
        null=True,
    )
    lunch_notes = models.CharField(
        verbose_name="Lunch Notes",
        max_length=250,
        blank=True,
        null=True,
    )
    dinner = models.CharField(
        verbose_name="Dinner",
        max_length=250,
        blank=True,
        null=True,
    )
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
    dinner_notes = models.CharField(
        verbose_name="Dinner Notes",
        max_length=250,
        blank=True,
        null=True,
    )
    favorite_flowers = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def save(self, *args, **kwargs):
        if self.breakfast and "NONE" in self.breakfast:
            self.breakfast = "[NONE]"
        if self.lunch and "NONE" in self.lunch:
            self.lunch = "[NONE]"
        if self.dinner and "NONE" in self.dinner:
            self.dinner = "[NONE]"

        return super(ShortJetPreferenceSheet, self).save(*args, **kwargs)

    @property
    def is_complete(self):
        required_fields = [
            "dietary_restrictions",
            "breakfast",
            "lunch",
            "dinner",
        ]
        return all(getattr(self, field) is not None for field in required_fields)

    def __str__(self):
        if self.guest.first_name and self.guest.last_name:
            return f"{self.guest.first_name} {self.guest.last_name}"
        self.guest.email

    class Meta:
        verbose_name = "Short Jet Preference Sheet"
        verbose_name_plural = "Short Jet Preference Sheets"


class LongJetPreferenceSheet(models.Model):
    class BreakfastChoices(models.TextChoices):
        EGG_SANDIWCH = ("EGG_SANDIWCH", "Egg Sandiwch")
        PASTRY_BASKET = ("PASTRY_BASKET", "Pastry Basket")
        YOGURT = ("YOGURT", "Yogurt")
        AVOCADO_TOAST = ("AVOCADO_TOAST", "Avocado Toast")
        MUFFINS = ("MUFFINS", "Muffins")
        DOUGHNUTS = ("DOUGHNUTS", "Doughnuts")
        SMOOTHIES = ("SMOOTHIES", "Smoothies")
        NONE = ("NONE", "None")

    class LunchChoices(models.TextChoices):
        FRUIT_PLATTER = ("FRUIT_PLATTER", "Fruit Platter")
        SANDWICH = ("SANDWICH", "Sandwich (Specify below)")
        WRAP = ("WRAP", "Wrap (Specify below)")
        NONE = ("NONE", "None")

    class DinnerChoices(models.TextChoices):
        BEEF = ("BEEF", "Beef")
        FISH = ("FISH", "Fish")
        VEGETARIAN = ("VEGETARIAN", "Vegetarian")
        CHICKEN = ("CHICKEN", "Chicken")
        NONE = ("NONE", "None")

    class FreshSnacksChoices(models.TextChoices):
        HUMMUS_PITA = ("HUMMUS_PITA", "Hummus & Pita")
        VEGGIE_PLATTER = ("VEGGIE_PLATTER", "Veggie Platter")
        CHIPS_DIP = ("CHIPS_DIP", "Chips & Dip")
        MEAT_CHEESE_PLATTER = ("MEAT_CHEESE_PLATTER", "Meat & Cheese Platter")
        FRUIT_PLATTER = ("FRUIT_PLATTER", "Fruit Platter")
        NONE = ("NONE", "None")

    class PantrySnacksChoices(models.TextChoices):
        PROTEIN_BARS = ("PROTEIN_BARS", "Protein Bars")
        NUTS_SEEDS = ("NUTS_SEEDS", "Nuts & Seeds")
        POPCORN = ("POPCORN", "Popcorn")
        DRIED_FRUIT = ("DRIED_FRUIT", "Dried Fruit")
        BISCUITS = ("BISCUITS", "Biscuits")
        NONE = ("NONE", "None")

    guest = models.OneToOneField(
        "charter.GuestDetail",
        verbose_name="Guest",
        related_name="long_jet_preference",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    dietary_restrictions = models.CharField(
        verbose_name="Dietary Restrictions",
        choices=DietaryRestrictionChoices.choices,
        max_length=50,
        null=True,
        blank=True,
    )
    dietary_restrictions_notes = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    dietary_restrictions_other_notes = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    breakfast = models.CharField(
        verbose_name="Breakfast",
        max_length=250,
        blank=True,
        null=True,
    )
    breakfast_notes = models.CharField(
        verbose_name="Breakfast Notes",
        max_length=250,
        blank=True,
        null=True,
    )
    lunch = models.CharField(
        verbose_name="Lunch",
        max_length=250,
        blank=True,
        null=True,
    )
    lunch_notes = models.CharField(
        verbose_name="Lunch Notes",
        max_length=250,
        blank=True,
        null=True,
    )
    dinner = models.CharField(
        verbose_name="Dinner",
        max_length=250,
        blank=True,
        null=True,
    )
    dinner_notes = models.CharField(
        verbose_name="Dinner Notes",
        max_length=250,
        blank=True,
        null=True,
    )
    fresh_snacks = models.CharField(
        verbose_name="Fresh Snacks",
        max_length=250,
        blank=True,
        null=True,
    )
    fresh_snacks_notes = models.CharField(
        verbose_name="Fresh Snacks Notes",
        max_length=250,
        blank=True,
        null=True,
    )
    pantry_snacks = models.CharField(
        verbose_name="Pantry Snacks",
        max_length=250,
        blank=True,
        null=True,
    )
    pantry_snacks_notes = models.CharField(
        verbose_name="Pantry Snacks Notes",
        max_length=250,
        blank=True,
        null=True,
    )
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
    favorite_flowers = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def save(self, *args, **kwargs):
        if self.breakfast and "NONE" in self.breakfast:
            self.breakfast = "[NONE]"
        if self.lunch and "NONE" in self.lunch:
            self.lunch = "[NONE]"
        if self.dinner and "NONE" in self.dinner:
            self.dinner = "[NONE]"
        if self.fresh_snacks and "NONE" in self.fresh_snacks:
            self.fresh_snacks = "[NONE]"
        if self.pantry_snacks and "NONE" in self.pantry_snacks:
            self.pantry_snacks = "[NONE]"

        return super(LongJetPreferenceSheet, self).save(*args, **kwargs)

    @property
    def is_complete(self):
        required_fields = [
            "dietary_restrictions",
            "breakfast",
            "lunch",
            "dinner",
            "fresh_snacks",
            "pantry_snacks",
        ]
        return all(getattr(self, field) is not None for field in required_fields)

    def __str__(self):
        if self.guest.first_name and self.guest.last_name:
            return f"{self.guest.first_name} {self.guest.last_name}"
        self.guest.email

    class Meta:
        verbose_name = "Long Jet Preference Sheet"
        verbose_name_plural = "Long Jet Preference Sheets"
