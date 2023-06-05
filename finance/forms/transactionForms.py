from django import forms
from finance.models import Transaction

class CreateTransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = '__all__'