# Generated by Django 4.1.4 on 2023-09-14 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0059_discplinarymanagement"),
    ]

    operations = [
        migrations.CreateModel(
            name="Bank",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("bank_code", models.CharField(max_length=10)),
                ("bank_name", models.CharField(max_length=100)),
                ("branch_code", models.CharField(max_length=10)),
                ("branch_name", models.CharField(max_length=100)),
                ("physical_address", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="PaymentMethods",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("code", models.CharField(max_length=100, null=True)),
                ("name", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=100)),
                ("transaction_reference_required", models.CharField(max_length=100)),
                ("unit_of_measure_required", models.CharField(max_length=100)),
                ("on_hold_disable_posting_on_item", models.CharField(max_length=100)),
                ("gl_account", models.CharField(max_length=100)),
                ("notes", models.TextField(null=True)),
                (
                    "default_bank_account",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.bank",
                    ),
                ),
            ],
        ),
    ]
