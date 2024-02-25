from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from finance.models import BillingItem

class BillingItemForm(forms.ModelForm):
    priority = forms.IntegerField(
        label="Priority",
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=True,
        min_value=1,  # Minimum value
        max_value=9   # Maximum value
    )
    default_amount = forms.CharField(
        label="Default Amount",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
    )

    code = forms.CharField(
        label="Code",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    description = forms.CharField(
        label="Description",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    category = forms.CharField(
        label="Category",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    occurrence = forms.CharField(
        label="Occurrence",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    applicability = forms.CharField(
        label="Applicability",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    required_percentage = forms.CharField(
        label="Required Percentage",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    on_hold_disable_posting_on_item = forms.CharField(
        label="On Hold Disable Posting on Item",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    gl_account = forms.CharField(
        label="GL Account",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    gl_statement_prefix = forms.CharField(
        label="GL Statement Prefix",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    notes = forms.CharField(
        label="Notes",
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=False
    )

    class Meta:
        model = BillingItem
        fields = '__all__'



class UpdateBillingItemForm(forms.ModelForm):
    priority = forms.IntegerField(
        label="Priority",
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=True
    )
    default_amount = forms.CharField(
        label="Default Amount",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
    )

    code = forms.CharField(
        label="Code",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    description = forms.CharField(
        label="Description",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    category = forms.CharField(
        label="Category",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    occurrence = forms.CharField(
        label="Occurrence",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    applicability = forms.CharField(
        label="Applicability",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    required_percentage = forms.CharField(
        label="Required Percentage",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    on_hold_disable_posting_on_item = forms.CharField(
        label="On Hold Disable Posting on Item",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    gl_account = forms.CharField(
        label="GL Account",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    gl_statement_prefix = forms.CharField(
        label="GL Statement Prefix",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    notes = forms.CharField(
        label="Notes",
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=False
    )

    class Meta:
        model = BillingItem
        fields = '__all__'