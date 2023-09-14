from django import forms
from core.models import Campus, EcActivities

class EcActivitiesForm(forms.ModelForm):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Both', 'Both'),
    ]

    code = forms.CharField(label="Code", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    description = forms.CharField(label="Description", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES, widget=forms.Select(attrs={"class": "form-control"}),required=False)
    campus = forms.ModelChoiceField(label="Campus", queryset=Campus.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)

    class Meta:
        model = EcActivities
        fields = '__all__'


class EditEcActivitiesForm(forms.ModelForm):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Both', 'Both'),
    ]

    code = forms.CharField(label="Code", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    description = forms.CharField(label="Description", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES, widget=forms.Select(attrs={"class": "form-control"}),required=False)
    campus = forms.ModelChoiceField(label="Campus", queryset=Campus.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)

    class Meta:
        model = EcActivities
        fields = '__all__'