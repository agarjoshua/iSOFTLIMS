# Generated by Django 4.1.4 on 2023-07-19 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0047_alter_department_options_department_created_at_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={"ordering": ["id"]},
        ),
    ]