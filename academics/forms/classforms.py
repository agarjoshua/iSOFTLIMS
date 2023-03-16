from django import forms
from academics.models import Class, Grade, Session
from core.models import Teacher


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['class_name', 'class_code', 'teacher', 'grade', 'session_id', 'is_elective', 'start_date', 'end_date', 'cost']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ClassSearchForm(forms.Form):
    class_name = forms.CharField(label='Class Name', max_length=50, required=False)
    class_code = forms.CharField(label='Class Code', max_length=50, required=False)
    teacher = forms.ModelChoiceField(label='Teacher', queryset=Teacher.objects.all(), required=False)
    grade = forms.ModelChoiceField(label='Grade', queryset=Grade.objects.all(), required=False)
    session_id = forms.ModelChoiceField(label='Session', queryset=Session.objects.all(), required=False)
    is_elective = forms.BooleanField(label='Is Elective?', required=False)
    start_date = forms.DateField(label='Start Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    cost_min = forms.IntegerField(label='Minimum Cost', required=False)
    cost_max = forms.IntegerField(label='Maximum Cost', required=False)