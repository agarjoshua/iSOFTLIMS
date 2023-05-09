# Generated by Django 4.1.4 on 2023-04-30 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_remove_admin_institution"),
    ]

    operations = [
        migrations.AddField(
            model_name="admin",
            name="institution",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.institution",
            ),
        ),
    ]
