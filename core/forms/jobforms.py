#create forms for the job model

from django import forms
from django.forms import ModelForm
from core.models import Job

class JobForm(ModelForm):

    code = forms.CharField(label="Code", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="Description", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    job_type = forms.CharField(label="Job Type", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    start_date = forms.DateField(label="Start Date", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    end_date = forms.DateField(label="End Date", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    gl_account = forms.CharField(label="GL Account", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    notes = forms.CharField(label="Notes", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Job
        fields = '__all__'


class EditJobForm(ModelForm):

    code = forms.CharField(label="Code", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="Description", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    job_type = forms.CharField(label="Job Type", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    start_date = forms.DateField(label="Start Date", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    end_date = forms.DateField(label="End Date", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    gl_account = forms.CharField(label="GL Account", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    notes = forms.CharField(label="Notes", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Job
        fields = '__all__'