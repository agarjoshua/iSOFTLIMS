# Generated by Django 4.1.4 on 2023-05-18 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0033_interfacultytransferapprovalworklow_current_course_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="interfacultytransferapprovalworklow",
            name="applicant",
            field=models.ForeignKey(
                default=5,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.students",
            ),
            preserve_default=False,
        ),
    ]
