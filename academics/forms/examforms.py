from django import forms
from academics.models import Exam, ExamType

class ExamForm(forms.ModelForm):
    exam_type = forms.ModelChoiceField(queryset=ExamType.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Exam
        fields = ['name', 'exam_type', 'exam_date', 'is_compulsory', 'exam_class']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control'}),
            'is_compulsory': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'exam_class': forms.TextInput(attrs={'class': 'form-control'}),
        }
