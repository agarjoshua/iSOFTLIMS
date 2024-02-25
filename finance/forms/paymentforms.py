from django import forms

from finance.models import PaymentMethods, Bank, Transactiontype, Transaction

class BankForm(forms.ModelForm):
    bank_code = forms.CharField(label="Bank Code", max_length=10, widget=forms.TextInput(attrs={"class": "form-control"}))
    bank_name = forms.CharField(label="Bank Name", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    physical_address = forms.CharField(label="Physical Address", max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))
    branch_code = forms.CharField(label="Branch Code", max_length=10, widget=forms.TextInput(attrs={"class": "form-control"}))
    branch_name = forms.CharField(label="Branch Name", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    physical_address = forms.CharField(label="Branch Physical Address", max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Bank
        fields = '__all__'

class BankUpdateForm(forms.ModelForm):
    bank_code = forms.CharField(label="Bank Code", max_length=10, widget=forms.TextInput(attrs={"class": "form-control"}))
    bank_name = forms.CharField(label="Bank Name", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    physical_address = forms.CharField(label="Physical Address", max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))
    branch_code = forms.CharField(label="Branch Code", max_length=10, widget=forms.TextInput(attrs={"class": "form-control"}))
    branch_name = forms.CharField(label="Branch Name", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    physical_address = forms.CharField(label="Branch Physical Address", max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Bank
        fields = '__all__'
        # exclude = ['bank_code', 'bank_name', 'physical_address', 'branch_code', 'branch_name', 'branch_physical_address']


class PaymentMethodsForm(forms.ModelForm):
    code = forms.CharField(label="Code", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="Description", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    default_bank_account = forms.ModelChoiceField(label="Default Bank Account", queryset=Bank.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-control"}))
    transaction_reference_required = forms.CharField(label="Transaction Reference Required", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    unit_of_measure_required = forms.CharField(label="Unit of Measure Required", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    on_hold_disable_posting_on_item = forms.CharField(label="On Hold Disable Posting on Item", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    gl_account = forms.CharField(label="GL Account", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    notes = forms.CharField(label="Notes", max_length=255, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = PaymentMethods
        fields = '__all__'


class PaymentMethodsUpdateForm(forms.ModelForm):
    code = forms.CharField(label="Code", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="Description", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    default_bank_account = forms.ModelChoiceField(label="Default Bank Account", queryset=Bank.objects.all(), required=False, widget=forms.Select(attrs={"class": "form-control"}))
    transaction_reference_required = forms.CharField(label="Transaction Reference Required", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    unit_of_measure_required = forms.CharField(label="Unit of Measure Required", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    on_hold_disable_posting_on_item = forms.CharField(label="On Hold Disable Posting on Item", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    gl_account = forms.CharField(label="GL Account", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    notes = forms.CharField(label="Notes", max_length=255, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = PaymentMethods
        fields = '__all__'
        # exclude = ['code', 'name', 'description', 'default_bank_account', 'transaction_reference_required', 'unit_of_measure_required', 'on_hold_disable_posting_on_item', 'gl_account', 'notes']