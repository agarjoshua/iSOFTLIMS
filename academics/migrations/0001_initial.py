# Generated by Django 4.1.4 on 2023-01-16 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Courses",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("course_name", models.CharField(max_length=255)),
                ("cost", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Grade",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("grade_name", models.CharField(max_length=255)),
                ("cost", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="SessionYearModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("session_start_year", models.DateField()),
                ("session_end_year", models.DateField()),
            ],
        ),
    ]
