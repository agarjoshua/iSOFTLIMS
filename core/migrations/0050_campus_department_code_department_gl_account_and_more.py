# Generated by Django 4.1.4 on 2023-08-18 08:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0049_admin_profile_pic"),
    ]

    operations = [
        migrations.CreateModel(
            name="Campus",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "institution_code",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("campus_code", models.CharField(max_length=30, null=True)),
                ("name", models.CharField(max_length=30)),
                ("physical_address", models.CharField(max_length=255, null=True)),
                ("notes", models.TextField(null=True)),
                ("gl_account", models.CharField(max_length=255, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[(1, "Active"), (2, "Inactive")],
                        default="1",
                        max_length=255,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "institution",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.institution",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="department",
            name="code",
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="department",
            name="gl_account",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="department",
            name="notes",
            field=models.TextField(null=True),
        ),
        migrations.CreateModel(
            name="School",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("code", models.CharField(max_length=30, null=True)),
                ("name", models.CharField(max_length=30)),
                ("description", models.CharField(max_length=30)),
                ("gl_account", models.CharField(max_length=255, null=True)),
                ("notes", models.TextField(null=True)),
                (
                    "campus",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.campus",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Program",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30)),
                ("code", models.CharField(max_length=30, null=True)),
                ("description", models.CharField(max_length=30)),
                ("duration", models.CharField(max_length=30)),
                ("number_of_terms", models.CharField(max_length=30)),
                ("current_term", models.CharField(max_length=30)),
                ("minimum_examinable_subjects", models.CharField(max_length=30)),
                ("maximum_examinable_subjects", models.CharField(max_length=30)),
                ("final_exam_marks_based_on", models.CharField(max_length=30)),
                ("mean_mark_to_advance_to_next_level", models.CharField(max_length=30)),
                ("curriculum_description", models.CharField(max_length=30)),
                ("class_progression", models.CharField(max_length=30)),
                ("progression_next_level", models.CharField(max_length=30)),
                ("gl_account", models.CharField(max_length=30)),
                ("notes", models.TextField(null=True)),
                (
                    "school",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.school",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CurriculumSystem",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("code", models.CharField(max_length=30, null=True)),
                ("name", models.CharField(max_length=30)),
                ("description", models.CharField(max_length=30)),
                ("study_period", models.CharField(max_length=30)),
                ("levels", models.CharField(max_length=30)),
                ("campuses", models.CharField(max_length=30)),
                ("gl_account", models.CharField(max_length=30)),
                ("notes", models.TextField(null=True)),
                (
                    "school",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.school",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("code", models.CharField(max_length=30, null=True)),
                ("name", models.CharField(max_length=30)),
                ("description", models.CharField(max_length=30)),
                ("duration", models.CharField(max_length=30)),
                ("number_of_terms", models.CharField(max_length=30)),
                ("current_term", models.CharField(max_length=30)),
                ("minimum_examinable_subjects", models.CharField(max_length=30)),
                ("maximum_examinable_subjects", models.CharField(max_length=30)),
                ("final_exam_marks_based_on", models.CharField(max_length=30)),
                ("mean_mark_to_advance_to_next_level", models.CharField(max_length=30)),
                ("curriculum_description", models.CharField(max_length=30)),
                ("class_progression", models.CharField(max_length=30)),
                ("progression_next_level", models.CharField(max_length=30)),
                ("gl_account", models.CharField(max_length=30)),
                ("notes", models.TextField(null=True)),
                (
                    "school",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.school",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="department",
            name="campus",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.campus",
            ),
        ),
        migrations.AddField(
            model_name="department",
            name="school",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.school",
            ),
        ),
    ]