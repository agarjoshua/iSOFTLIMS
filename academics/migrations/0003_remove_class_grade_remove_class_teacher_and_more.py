# Generated by Django 4.1.4 on 2023-03-23 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("academics", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="class",
            name="grade",
        ),
        migrations.RemoveField(
            model_name="class",
            name="teacher",
        ),
        migrations.RemoveField(
            model_name="enrollment",
            name="student",
        ),
    ]
