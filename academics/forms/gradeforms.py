from django import forms
from academics.models import GradeLevel
from core.models import Teacher

class ClassGradeForm(forms.ModelForm):

    # teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())
    # created_at = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


    class Meta: 
        model = GradeLevel
        fields = '__all__'

class GradeEditForm(forms.ModelForm):
    class Meta:
        model = GradeLevel
        fields = ('grade_name', 'cost', 'compulsory_classes')