# Generated by Django 4.1.4 on 2023-05-02 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_remove_applicant_admin_applicant_applicant"),
    ]

    operations = [
        migrations.CreateModel(
            name="StaffType",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="staff",
            name="institution",
        ),
        migrations.AddField(
            model_name="staff",
            name="email",
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="staff",
            name="telephone",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="staff",
            name="staff_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="core.stafftype"
            ),
        ),
    ]
