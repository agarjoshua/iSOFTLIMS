from django import forms
from academics.models import Course
from core.models import BillingTemplate, CurriculumSystem, FeeItem, Program, School

class BillingTemplateForm(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    faculty_or_school = forms.ModelChoiceField(label="Faculty or School", queryset=School.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    program = forms.ModelChoiceField(label="Program", queryset=Program.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    system = forms.ModelChoiceField(label="System", queryset=CurriculumSystem.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    course = forms.ModelChoiceField(label="Course", queryset=Course.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    class_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    sponsorship_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    year_of_study = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    fee_item = forms.ModelChoiceField(label="Fee Item", queryset=FeeItem.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)

    fee_item_amount = forms.IntegerField(label="Fee Item Ammount", widget=forms.TextInput(attrs={"class": "form-control"}), required=False)

    gl_statement_prefix = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    notes = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = BillingTemplate
        fields = '__all__'


class EditBillingTemplateForm(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    faculty_or_school = forms.ModelChoiceField(label="Faculty or School", queryset=School.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    program = forms.ModelChoiceField(label="Program", queryset=Program.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    system = forms.ModelChoiceField(label="System", queryset=CurriculumSystem.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    course = forms.ModelChoiceField(label="Course", queryset=Course.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    class_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    sponsorship_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    year_of_study = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    fee_item = forms.ModelChoiceField(label="Fee Item", queryset=FeeItem.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)

    fee_item_amount = forms.IntegerField(label="Fee Item Ammount", widget=forms.TextInput(attrs={"class": "form-control"}), required=False)

    gl_statement_prefix = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    notes = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = BillingTemplate
        fields = '__all__'