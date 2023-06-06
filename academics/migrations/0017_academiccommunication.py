# Generated by Django 4.1.4 on 2023-06-06 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("academics", "0016_classattendance"),
    ]

    operations = [
        migrations.CreateModel(
            name="AcademicCommunication",
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
                ("title", models.CharField(max_length=255)),
                ("body", models.CharField(max_length=255)),
                (
                    "communication_method",
                    models.CharField(
                        choices=[
                            ("sms", "SMS"),
                            ("email", "Email"),
                            ("notice", "General Notice"),
                        ],
                        default="email",
                        max_length=10,
                    ),
                ),
            ],
        ),
    ]
