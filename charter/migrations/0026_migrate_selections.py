# Generated by Django 3.2.9 on 2022-01-19 18:38

from django.db import migrations


def convert_foreign_keys(apps, schema_editor):
    MealAndRoomPreferences = apps.get_model("charter", "MealAndRoomPreferences")

    for instance in MealAndRoomPreferences.objects.all():
        instance.breakfast_selection = instance.breakfast_selections.last()
        instance.lunch_selection = instance.lunch_selections.last()
        instance.dinner_selection = instance.dinner_selections.last()
        instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ("charter", "0025_convert_meal_and_room_preferences"),
    ]

    operations = [migrations.RunPython(convert_foreign_keys)]