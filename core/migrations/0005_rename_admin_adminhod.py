# Generated by Django 4.1.4 on 2022-12-13 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_remove_admin_institution_remove_staff_institution_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Admin",
            new_name="AdminHOD",
        ),
    ]
