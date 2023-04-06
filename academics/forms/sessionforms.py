from django import forms
from academics.models import Enrollment

class EnrollmentCreateForm(forms.ModelForm):
    class Meta: 
        model = Enrollment
        fields = '__all__'
