# Generated by Django 4.1.4 on 2023-05-02 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_applicant_admin"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="applicant",
            name="admin",
        ),
        migrations.AddField(
            model_name="applicant",
            name="applicant",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]