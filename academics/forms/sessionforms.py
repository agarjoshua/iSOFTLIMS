from django import forms
from academics.models import Enrollment, Session

class EnrollmentCreateForm(forms.ModelForm):
    class Meta: 
        model = Enrollment
        fields = '__all__'



class SessionEditForm(forms.ModelForm):

    session_start_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'})
    )
    session_end_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Session
        fields = ('session_start_date', 'session_end_date', 'is_current')