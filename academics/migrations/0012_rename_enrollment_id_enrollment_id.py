# Generated by Django 4.1.4 on 2023-04-03 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("academics", "0011_enrollment_is_active"),
    ]

    operations = [
        migrations.RenameField(
            model_name="enrollment",
            old_name="enrollment_id",
            new_name="id",
        ),
    ]
