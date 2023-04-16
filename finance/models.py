# Create your models here.
from django.db import models

# from core.models import Students,Guardian, Admin, Session

# Create your models here.
class Transaction(models.Model):
    # Time, student, Parents(Guardian), Form of payment(Bank, M-pesa), Ammount paid

    TRANSACTION_TYPES = [
        ("payyment", "fee_payment"),
        ("charge", "fee_charge"),
        ("otherr", "other"),
    ]
    PAYMENT_TYPES = [
        ("mobile_money", "mobile_money"),
        ("bank", "bank"),
        ("other", "other"),
    ]

    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(
        'core.Students', on_delete=models.CASCADE, null=True
    )
    type = models.CharField(max_length=255, choices=TRANSACTION_TYPES, default="other")
    form_of_payment = models.CharField(
        max_length=255, choices=PAYMENT_TYPES, default="other"
    )
    ammount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.id


class Fee(models.Model):
    # Structure, Schedule(period for charging),
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    session = models.ForeignKey(
        'academics.Session', on_delete=models.CASCADE, null=True
    )
    ammount = models.IntegerField()
    is_recurrent = models.BooleanField(default=False)
    billed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
