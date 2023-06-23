# Generated by Django 4.1.4 on 2023-05-08 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0020_remove_students_institution_students_degree_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="students",
            name="degree_name",
        ),
        migrations.RemoveField(
            model_name="students",
            name="department",
        ),
        migrations.RemoveField(
            model_name="students",
            name="faculty",
        ),
        migrations.RemoveField(
            model_name="students",
            name="field_of_study",
        ),
        migrations.AddField(
            model_name="students",
            name="institution",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.institution",
            ),
        ),
    ]