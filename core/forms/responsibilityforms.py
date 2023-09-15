from django import forms

from core.models import CustomUser, Job
from core.models import UserResponsibility
# from django_select2.forms import ModelSelect2Widget

class ResponsibilityForm(forms.ModelForm):
    code = forms.CharField(label="Code", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    name = forms.CharField(label="Name", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="Description", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    user = forms.ModelChoiceField(label="User", queryset=CustomUser.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))
    # user = forms.ModelChoiceField(
    # label="User",
    # queryset=CustomUser.objects.all(),
    # widget=ModelSelect2Widget(
    #     model=CustomUser,
    #     search_fields=['username__icontains'],
    #     attrs={'class': 'form-control'}
    # )
    # )
    job = forms.ModelChoiceField(label="Job", queryset=Job.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = UserResponsibility
        fields = '__all__'


class EditResponsibilityForm(forms.ModelForm):
    code = forms.CharField(label="Code", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    name = forms.CharField(label="Name", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="Description", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    user = forms.ModelChoiceField(label="User", queryset=CustomUser.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))
    job = forms.ModelChoiceField(label="Job", queryset=Job.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = UserResponsibility
        fields = '__all__'
