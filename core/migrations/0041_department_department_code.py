# Generated by Django 4.1.4 on 2023-06-22 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0040_alter_institution_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="department",
            name="department_code",
            field=models.CharField(max_length=30, null=True),
        ),
    ]
