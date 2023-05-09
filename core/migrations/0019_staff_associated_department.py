# Generated by Django 4.1.4 on 2023-05-04 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0018_hod_associated_department"),
    ]

    operations = [
        migrations.AddField(
            model_name="staff",
            name="associated_department",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.department",
            ),
        ),
    ]
