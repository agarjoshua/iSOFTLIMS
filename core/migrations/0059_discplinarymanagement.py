# Generated by Django 4.1.4 on 2023-09-14 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0058_userresponsibility"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiscplinaryManagement",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("displinary_action", models.CharField(max_length=255)),
                ("discplinary_case_notes", models.CharField(max_length=255)),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("resumption_date", models.DateTimeField()),
                ("notes", models.CharField(max_length=255)),
                (
                    "subject",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]