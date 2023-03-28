from django import forms
from academics.models import Grade
from core.models import Teacher

class ClassGradeForm(forms.ModelForm):

    # teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())
    # created_at = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


    class Meta: 
        model = Grade
        fields = '__all__'

class GradeEditForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('grade_name', 'cost', 'compulsory_classes')