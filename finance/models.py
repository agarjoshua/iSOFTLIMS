# Create your models here.
from django.db import models

# from core.models import Students,Guardian, Admin, Session

# Create your models here.

class Transactiontype(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Transaction(models.Model):
    # Time, student, Parents(Guardian), Form of payment(Bank, M-pesa), Ammount paid
    id = models.AutoField(primary_key=True)
    transaction_code = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    associated_user = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, null=True)
    transaction_type = models.ForeignKey(Transactiontype, on_delete=models.DO_NOTHING)
    form_of_payment = models.CharField(max_length=255)
    ammount_paid = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateTimeField(auto_now=True)
    confirmed = models.BooleanField(default=False)
    Payee= models.CharField(max_length=255, null=True)
    Payer= models.CharField(max_length=255, null=True)
    comments = models.CharField(max_length=255, null=True)
    other_resources = models.FileField(upload_to='media/account_files', blank=True)
    receipt_image = models.ImageField(upload_to='media/transaction_images', blank=True)

    def __str__(self):
        return f"Transaction ID: {self.transaction_code}"


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
 