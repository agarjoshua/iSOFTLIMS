from django import forms
from academics.models import ClusterClass, GradeLevel
from core.models import Teacher

class ClassGradeForm(forms.ModelForm):

    compulsory_classes = forms.ModelChoiceField(queryset=ClusterClass.objects.all(), label='Compulsory Cluster')

    class Meta: 
        model = GradeLevel
        fields = '__all__'

class GradeEditForm(forms.ModelForm):
    class Meta:
        model = GradeLevel
        fields = ('grade_name', 'cost', 'compulsory_classes')