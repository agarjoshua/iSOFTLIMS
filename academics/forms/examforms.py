from django import forms
from academics.models import Exam, ExamType, GradeRange, Class

class ExamForm(forms.ModelForm):
    exam_type = forms.ModelChoiceField(queryset=ExamType.objects.all(), widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}))
    exam_class = forms.ModelChoiceField(queryset=Class.objects.all(), widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}))
    class Meta:
        model = Exam
        fields = ['name', 'exam_type', 'exam_date', 'is_compulsory', 'exam_class']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
            'exam_type': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'exam_class': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            # 'is_compulsory': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ExamTypeForm(forms.ModelForm):
    class Meta:
        model = ExamType
        fields = '__all__'


class GradeRangeForm(forms.ModelForm):

    exam = forms.ModelChoiceField(queryset=Exam.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    GRADE_CHOICE=(('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F'))
    institution_category = forms.ChoiceField(choices=GRADE_CHOICE, widget=forms.ChoiceField)
    class Meta:
        model = GradeRange
        fields = ['exam','grade','min_score','max_score']

