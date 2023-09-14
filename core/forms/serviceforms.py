from django import forms
from core.models import Service


class ServiceForm(forms.ModelForm):

    code = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    description = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    service_unit_of_measure = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    rate = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    payment_plan = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    taxable = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    tax_rate = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    gl_account = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    notes = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))


    class Meta:
        model = Service
        fields = '__all__'


class EditServiceForm(forms.ModelForm):
    
    code = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    description = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    service_unit_of_measure = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    rate = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    payment_plan = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    taxable = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    tax_rate = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    gl_account = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    notes = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={"class":"form-control"}))


    class Meta:
        model = Service
        fields = '__all__'