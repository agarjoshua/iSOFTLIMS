# Generated by Django 4.1.4 on 2023-05-01 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_remove_students_bio_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="admin",
            name="admin_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.admintype",
            ),
        ),
    ]