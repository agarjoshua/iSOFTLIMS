from django import forms
from academics.models import AcademicCommunications


class AcademicCommunicationForm(forms.ModelForm):
    class Meta:
        model = AcademicCommunications
        fields = '__all__'