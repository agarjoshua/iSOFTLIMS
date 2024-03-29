# Generated by Django 4.1.4 on 2023-09-14 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0055_service"),
    ]

    operations = [
        migrations.CreateModel(
            name="EcActivities",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=100, null=True)),
                ("description", models.CharField(max_length=100)),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Both", "Both"),
                        ],
                        max_length=10,
                    ),
                ),
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
    ]
