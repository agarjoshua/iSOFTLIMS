#create a form for the school model
# SchoolForm
import json
from django import forms
from core.models import School, Campus

class SchoolForm(forms.Form):
    code = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    description = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    # campus = forms.ModelChoiceField(queryset=Campus.objects.all(), label="Campus", widget=forms.Select(attrs={"class":"form-control"}))
    gl_account = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    notes = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    STATUS = [(1, "Active"), (2, "Inactive")]
    status = forms.TypedChoiceField(choices=STATUS, coerce=int, widget=forms.Select(attrs={"class": "form-control"}))


    def save(self, commit=True):
        school = School()
        school.code = self.cleaned_data['code']
        school.name = self.cleaned_data['name']
        school.description = self.cleaned_data['description']
        # school.campus = self.campus # type: ignore
        school.notes = self.cleaned_data['notes']
        school.gl_account = self.cleaned_data['gl_account']
        school.status = self.cleaned_data['status']
        if commit:
            school.save()
        return school

    
    def update(self, school, commit=True):
        school.code = self.cleaned_data['code']
        school.name = self.cleaned_data['name']
        school.description = self.cleaned_data['description']
        # school.campus = self.campus # type: ignore
        school.notes = self.cleaned_data['notes']
        school.gl_account = self.cleaned_data['gl_account']
        school.status = self.cleaned_data['status']
        if commit:
            school.save()
        return school

    
    def toJson(self):
        return json.dumps(self.cleaned_data)
    def __unicode__(self):
        return self.cleaned_data['name']