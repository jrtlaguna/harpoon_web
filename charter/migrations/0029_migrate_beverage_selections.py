# Generated by Django 3.2.9 on 2022-01-19 19:17

from django.db import migrations


def migrate_beverage_selections(apps, schema_editor):

    OtherServices = apps.get_model("charter", "OtherServices")
    MilkSelection = apps.get_model("charter", "MilkSelection")
    CoffeeSelection = apps.get_model("charter", "CoffeeSelection")
    TeaSelection = apps.get_model("charter", "TeaSelection")
    WaterSelection = apps.get_model("charter", "WaterSelection")
    JuiceSelection = apps.get_model("charter", "JuiceSelection")
    SodasAndMixersSelection = apps.get_model("charter", "SodasAndMixersSelection")
    AddOnsSelection = apps.get_model("charter", "AddOnsSelection")

    for instance in OtherServices.objects.all():
        instance.temp_field = instance.diet_services_sizes_preferences.last()
        instance.save()

    for instance in MilkSelection.objects.all():
        instance.temp_field = instance.beverages_and_alcoholic_preferences.last()
        instance.save()
    for instance in CoffeeSelection.objects.all():
        instance.temp_field = instance.beverages_and_alcoholic_preferences.last()
        instance.save()
    for instance in TeaSelection.objects.all():
        instance.temp_field = instance.beverages_and_alcoholic_preferences.last()
        instance.save()
    for instance in WaterSelection.objects.all():
        instance.temp_field = instance.beverages_and_alcoholic_preferences.last()
        instance.save()
    for instance in JuiceSelection.objects.all():
        instance.temp_field = instance.beverages_and_alcoholic_preferences.last()
        instance.save()
    for instance in SodasAndMixersSelection.objects.all():
        instance.temp_field = instance.beverages_and_alcoholic_preferences.last()
        instance.save()
    for instance in AddOnsSelection.objects.all():
        instance.temp_field = instance.beverages_and_alcoholic_preferences.last()
        instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ("charter", "0028_add_temp_one_to_one_field"),
    ]

    operations = [migrations.RunPython(migrate_beverage_selections)]
