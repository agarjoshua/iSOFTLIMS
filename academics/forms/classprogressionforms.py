# Create class progression forms:

# Path: academics/forms/classprogressionforms.py
from typing import Any
from django import forms
from academics.models import ClassProgression, ClusterClass, Course
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.forms import ValidationError
from django.forms import ModelChoiceField

from core.models import CurriculumSystem

class ClassProgressionForm(forms.ModelForm):
    #create fields from the studyprogression model
    code = forms.CharField(label="Code", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="Description", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    program = forms.CharField(label="Program", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    system = forms.ModelChoiceField(label="System", queryset=CurriculumSystem.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    course = forms.ModelChoiceField(label="Course", queryset=Course.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    number_of_progression_steps = forms.IntegerField(label="Number of Progression Steps", widget=forms.NumberInput(attrs={"class": "form-control"}), required=False)
    step = forms.CharField(label="Step", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    class_code = forms.CharField(label="Class Code", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)

    class Meta:
        model = ClassProgression
        fields = '__all__'


class Editclassprogressionform(forms.ModelForm):
    code = forms.CharField(label="Code", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="Description", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    program = forms.CharField(label="Program", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    system = forms.ModelChoiceField(label="System", queryset=CurriculumSystem.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    course = forms.ModelChoiceField(label="Course", queryset=Course.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    number_of_progression_steps = forms.IntegerField(label="Number of Progression Steps", widget=forms.NumberInput(attrs={"class": "form-control"}), required=False)
    step = forms.CharField(label="Step", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    class_code = forms.CharField(label="Class Code", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)

    class Meta:
        model = ClassProgression
        fields = '__all__'

