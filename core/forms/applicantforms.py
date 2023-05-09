from django import forms
from django.forms import ClearableFileInput, DateInput
from django.utils.translation import gettext_lazy as _
from core.models import Applicant

class ApplicantForm(forms.ModelForm):
    # department = forms.CharField(max_length=100)
    # concept_paper = forms.FileField()
    # masters_degree_type = forms.CharField(max_length=100)
    # masters_degree_title = forms.CharField(max_length=100)
    # start_date = forms.DateField(label="Session End", widget=DateInput(attrs={"class": "form-control"}))
    # expected_completion_date = forms.DateField(label="Session End", widget=DateInput(attrs={"class": "form-control"}))
    # mode_of_study = forms.CharField(max_length=100)
    # photo_1 = forms.FileField()
    # photo_2 = forms.FileField()
    # secondary_schools_attended = forms.CharField(widget=forms.Textarea)
    # university_education = forms.CharField(widget=forms.Textarea)
    # other_degrees_or_diploma = forms.CharField(widget=forms.Textarea)
    # research_experience = forms.CharField(widget=forms.Textarea)
    # employment_work_experience = forms.CharField(widget=forms.Textarea)
    # languages_spoken = forms.CharField(widget=forms.Textarea)
    # referee1_name = forms.CharField(max_length=100)
    # referee1_designation = forms.CharField(max_length=100)
    # referee1_address = forms.CharField(widget=forms.Textarea)
    # referee1_telephone = forms.CharField(max_length=20)
    # referee1_email = forms.EmailField()
    # referee2_name = forms.CharField(max_length=100)
    # referee2_designation = forms.CharField(max_length=100)
    # referee2_address = forms.CharField(widget=forms.Textarea)
    # referee2_telephone = forms.CharField(max_length=20)
    # referee2_email = forms.EmailField()
    # how_did_you_know_about_us = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Applicant
        fields = '__all__'
        widgets = {
            'concept_paper': ClearableFileInput(attrs={'multiple': False}),
            'photo_1': ClearableFileInput(attrs={'multiple': False}),
            'photo_2': ClearableFileInput(attrs={'multiple': False}),
            # 'start_date': forms.DateInput(attrs={'type': 'date'}),
            # 'expected_completion_date': forms.DateInput(attrs={'type': 'date'}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['concept_paper'].required = False
        self.fields['photo_1'].required = False
        self.fields['photo_2'].required = False

    def clean_concept_paper(self):
        concept_paper = self.cleaned_data['concept_paper']
        if concept_paper:
            # Check file size
            if concept_paper.size > 2 * 1024 * 1024:
                raise forms.ValidationError(_('File size must be under 2MB.'))
            # Check file type
            content_type = concept_paper.content_type.split('/')[0]
            if content_type not in ['application/pdf']:
                raise forms.ValidationError(_('Unsupported file type. Only PDF files are allowed.'))
        return concept_paper

    def clean_photo_1(self):
        photo_1 = self.cleaned_data['photo_1']
        if photo_1:
            # Check file size
            if photo_1.size > 2 * 1024 * 1024:
                raise forms.ValidationError(_('File size must be under 2MB.'))
            # Check file type
            content_type = photo_1.content_type.split('/')[0]
            if content_type not in ['image']:
                raise forms.ValidationError(_('Unsupported file type. Only image files are allowed.'))
        return photo_1

    def clean_photo_2(self):
        photo_2 = self.cleaned_data['photo_2']
        if photo_2:
            # Check file size
            if photo_2.size > 2 * 1024 * 1024:
                raise forms.ValidationError(_('File size must be under 2MB.'))
            # Check file type
            content_type = photo_2.content_type.split('/')[0]
            if content_type not in ['image']:
                raise forms.ValidationError(_('Unsupported file type. Only image files are allowed.'))
        return photo_2

