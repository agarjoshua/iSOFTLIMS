# Generated by Django 4.1.4 on 2023-06-22 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("academics", "0018_rename_academiccommunication_academiccommunications"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="compulsory_classes",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="academics.clusterclass",
            ),
        ),
    ]
