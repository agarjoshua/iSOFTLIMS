from django import forms
from finance.models import Transaction, Fee
# from models import Transaction,Fee

class TransactionForm(forms.ModelForm):

    student_id = forms.CharField(required=True, label="Students' Admission Number")
    transaction_details = forms.CharField(required=True, label='Transactions details')
    form_of_payment = forms.CharField(required=True, label='This will be automatic**')
    ammount_paid = forms.IntegerField(required=True, label='This will also be automatic')

    class Meta:
        model = Transaction
        fields = ('student_id','transaction_details','form_of_payment','ammount_paid')

class FeeCreationForm(forms.ModelForm):

    name = forms.CharField(required=True, label='Name of Invoice')
    start_period = forms.DateField(required=True, label='start period of session (in the format yyyy-mm-dd)')
    end_period = forms.DateField(required=True, label='end period of session (in the format yyyy-mm-dd)')
    ammount = forms.IntegerField(required=True, label='ammount')
    year = forms.IntegerField(required=True, label='financial year')
    grade = forms.CharField(required=True, label='grade year')
    renewable = forms.BooleanField(required=True, label='Renewable?')

    class Meta:
        model = Fee
        fields = ('name','start_period','end_period','ammount', 'year', 'grade','renewable')