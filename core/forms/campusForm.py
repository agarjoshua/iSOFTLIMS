
# Form for the model Campus
import json
from django import forms
from core.models import Campus

class CampusForm(forms.Form):

    # institution_code = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    campus_code = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    physical_address = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    notes = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    gl_account = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    STATUS = [(1, "Active"), (2, "Inactive")]
    status = forms.TypedChoiceField(choices=STATUS, coerce=int, widget=forms.Select(attrs={"class": "form-control"}))


    def save(self, commit=True):
        campus = Campus()
        campus.name = self.cleaned_data['name']
        campus.physical_address = self.cleaned_data['physical_address']
        campus.notes = self.cleaned_data['notes']
        campus.gl_account = self.cleaned_data['gl_account']
        campus.status = self.cleaned_data['status']
        if commit:
            campus.save()
        return campus

    
    def update(self, campus, commit=True):
        campus.name = self.cleaned_data['name']
        campus.physical_address = self.cleaned_data['physical_address']
        campus.notes = self.cleaned_data['notes']
        campus.gl_account = self.cleaned_data['gl_account']
        campus.status = self.cleaned_data['status']
        if commit:
            campus.save()
        return campus

    
    
    def toJson(self):
        return json.dumps(self.cleaned_data)
    def __unicode__(self):
        return self.cleaned_data['name']
    