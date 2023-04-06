from django import forms
from academics.models import Class, GradeLevel, Session
from core.models import Teacher
from django_select2.forms import Select2Widget
from django.core.exceptions import ValidationError

class ClassCreateForm(forms.ModelForm):

    gradelevel = forms.ModelMultipleChoiceField(queryset=GradeLevel.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Class
        fields = ['class_name', 'class_code', 'teacher', 'gradelevel', 'session_id', 'is_elective', 'start_date', 'end_date', 'cost']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ClassEditForm(forms.ModelForm):

    gradelevels = forms.ModelMultipleChoiceField(
        queryset=GradeLevel.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Class
        fields = ['class_name', 'class_code', 'teacher', 'gradelevel', 'session_id', 'is_elective', 'start_date', 'end_date', 'cost']
        # Use widgets to add attributes to form fields
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'teacher': Select2Widget(attrs={'class': 'form-control'}),
            'gradelevel': Select2Widget(attrs={'gradelevel': 'form-control'}),
            'session': Select2Widget(attrs={'session': 'form-control'}),
        }
        
    # Override the default labels for the form fields
    class_name = forms.CharField(label='Class Name')
    class_code = forms.CharField(label='Class Code')
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())
    gradelevel = forms.ModelChoiceField(queryset=GradeLevel.objects.all())
    session_id = forms.ModelChoiceField(queryset=Session.objects.all())
    is_elective = forms.BooleanField(label='Is Elective')
    start_date = forms.DateField(label='Start Date')
    end_date = forms.DateField(label='End Date')
    cost = forms.DecimalField(label='Cost')

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        cost = cleaned_data.get("cost")

        if start_date and end_date and start_date > end_date:
            raise ValidationError("Start date cannot be after end date.")
        
        if cost and cost <= 0:
            raise ValidationError("Cost must be a positive number.")



class ClassSearchForm(forms.Form):
    class_name = forms.CharField(label='Class Name', max_length=50, required=False)
    class_code = forms.CharField(label='Class Code', max_length=50, required=False)
    teacher = forms.ModelChoiceField(label='Teacher', queryset=Teacher.objects.all(), required=False)
    gradelevel = forms.ModelChoiceField(label='GradeLevel', queryset=GradeLevel.objects.all(), required=False)
    session_id = forms.ModelChoiceField(label='Session', queryset=Session.objects.all(), required=False)
    is_elective = forms.BooleanField(label='Is Elective?', required=False)
    start_date = forms.DateField(label='Start Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    cost_min = forms.IntegerField(label='Minimum Cost', required=False)
    cost_max = forms.IntegerField(label='Maximum Cost', required=False)