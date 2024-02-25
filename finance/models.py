# Create your models here.
from django.db import models

from core.models import CurriculumSystem, Program, School
from django.core.validators import MinValueValidator, MaxValueValidator

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


class Bank(models.Model):
    id = models.AutoField(primary_key=True)
    bank_code = models.CharField(max_length=10)
    bank_name = models.CharField(max_length=100)
    physical_address = models.CharField(max_length=255)
    branch_code = models.CharField(max_length=10)
    branch_name = models.CharField(max_length=100)
    physical_address = models.CharField(max_length=255)
    objects = models.Manager()

    def __str__(self):
        return self.bank_name

class PaymentMethods(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    default_bank_account = models.ForeignKey(Bank, on_delete=models.DO_NOTHING, null=True)
    transaction_reference_required = models.CharField(max_length=100)
    unit_of_measure_required = models.CharField(max_length=100)
    on_hold_disable_posting_on_item = models.CharField(max_length=100)
    gl_account = models.CharField(max_length=100)
    notes = models.TextField(null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
    
class BillingItem(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100)
    is_fee = models.BooleanField(default=False)
    category = models.CharField(max_length=100)
    occurrence = models.CharField(max_length=100)
    applicability = models.JSONField(null=True)
    priority = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])
    default_amount = models.CharField(max_length=100)
    required_percentage = models.CharField(max_length=100)
    on_hold_disable_posting_on_item = models.CharField(max_length=100)
    gl_account = models.CharField(max_length=100)
    gl_statement_prefix = models.CharField(max_length=100)
    notes = models.TextField(null=True)
    objects = models.Manager()

    def __str__(self):
        return self.code


class BillingTemplate(models.Model):
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    faculty_or_school = models.ForeignKey(School, on_delete=models.DO_NOTHING, null=True)
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING, null=True)
    system = models.ForeignKey(CurriculumSystem, on_delete=models.DO_NOTHING, null=True)
    course = models.ForeignKey("academics.Course", on_delete=models.DO_NOTHING, null=True)
    class_name = models.CharField(max_length=100)
    sponsorship_type = models.CharField(max_length=100)
    year_of_study = models.CharField(max_length=100)
    # billing_item = models.ForeignKey(BillingItem, on_delete=models.DO_NOTHING, null=True)
    fee_item_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gl_statement_prefix = models.CharField(max_length=100)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.code


class Fee(models.Model):
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
