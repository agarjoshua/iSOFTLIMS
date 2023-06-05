# Generated by Django 4.1.4 on 2023-05-30 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0004_transaction_transaction_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="Payee",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="transaction",
            name="Payer",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="transaction",
            name="comments",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
