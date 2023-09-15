from django import forms
from core.models import CustomUser, DiscplinaryManagement

class DisciplinaryManagementForm(forms.ModelForm):
    subject = forms.ModelChoiceField(label="Subject", queryset=CustomUser.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))
    displinary_action = forms.CharField(label="Disciplinary Action", max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))
    discplinary_case_notes = forms.CharField(label="Disciplinary Case Notes", max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))
    start_date = forms.DateTimeField(label="Start Date", widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}))
    end_date = forms.DateTimeField(label="End Date", widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}))
    resumption_date = forms.DateTimeField(label="Resumption Date", widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}))
    notes = forms.CharField(label="Notes", max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = DiscplinaryManagement
        fields = '__all__'


class EditDisciplinaryManagementForm(forms.ModelForm):
    subject = forms.ModelChoiceField(label="Subject", queryset=CustomUser.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))
    displinary_action = forms.CharField(label="Disciplinary Action", max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))
    discplinary_case_notes = forms.CharField(label="Disciplinary Case Notes", max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))
    start_date = forms.DateTimeField(label="Start Date", widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}))
    end_date = forms.DateTimeField(label="End Date", widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}))
    resumption_date = forms.DateTimeField(label="Resumption Date", widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}))
    notes = forms.CharField(label="Notes", max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = DiscplinaryManagement
        fields = '__all__'