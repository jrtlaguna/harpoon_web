# Generated by Django 3.2.9 on 2023-02-22 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admins", "0008_crewprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="crewprofile",
            name="profile_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="", verbose_name="Profile Picture"
            ),
        ),
        migrations.AlterField(
            model_name="crewprofile",
            name="about",
            field=models.CharField(
                blank=True, max_length=256, null=True, verbose_name="About"
            ),
        ),
        migrations.AlterField(
            model_name="crewprofile",
            name="interest",
            field=models.CharField(
                blank=True, max_length=256, null=True, verbose_name="Interest"
            ),
        ),
        migrations.AlterField(
            model_name="crewprofile",
            name="previous_yacht",
            field=models.CharField(
                blank=True, max_length=400, null=True, verbose_name="Previous Yacht"
            ),
        ),
    ]
