# Generated by Django 4.1.4 on 2023-01-09 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0018_hod_institution_teacher_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="institution",
            name="institution_cype",
            field=models.CharField(
                choices=[
                    ("1", "Preprimary"),
                    ("2", "Primary"),
                    ("3", "Secondary"),
                    ("4", "tertiary"),
                ],
                default="other",
                max_length=255,
            ),
        ),
    ]
