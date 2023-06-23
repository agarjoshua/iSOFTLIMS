# Generated by Django 4.1.4 on 2023-05-04 17:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0019_staff_associated_department"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="students",
            name="institution",
        ),
        migrations.AddField(
            model_name="students",
            name="degree_name",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="students",
            name="department",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="students",
            name="faculty",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="students",
            name="field_of_study",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]