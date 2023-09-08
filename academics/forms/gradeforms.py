from django import forms
from academics.models import ClusterClass, Course, GradeLevel
from core.models import CurriculumSystem, Teacher

class ClassGradeForm(forms.ModelForm):
    code = forms.CharField(label="Code", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    grade_name = forms.CharField(label="Grade Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    description = forms.CharField(label="Description", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    program = forms.CharField(label="Program", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    system = forms.ModelChoiceField(label="System", queryset=CurriculumSystem.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    course = forms.ModelChoiceField(label="Course", queryset=Course.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    class_progression_mean_grade_score = forms.CharField(label="Class Progression Mean Grade Score", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    class_capacity = forms.IntegerField(label="Class Capacity", widget=forms.NumberInput(attrs={"class": "form-control"}), required=False)
    students_teacher_ratio = forms.IntegerField(label="Students Teacher Ratio", widget=forms.NumberInput(attrs={"class": "form-control"}), required=False)
    assigned_class_capacity = forms.IntegerField(label="Assigned Class Capacity", widget=forms.NumberInput(attrs={"class": "form-control"}), required=False)
    number_of_streams = forms.IntegerField(label="Number of Streams", widget=forms.NumberInput(attrs={"class": "form-control"}), required=False)
    compulsory_classes = forms.ModelChoiceField(label="Compulsory Classes", queryset=ClusterClass.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    notes = forms.CharField(label="Notes", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)

    class Meta: 
        model = GradeLevel
        fields = '__all__'

class GradeEditForm(forms.ModelForm):

    code = forms.CharField(label="Code", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    grade_name = forms.CharField(label="Grade Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    description = forms.CharField(label="Description", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    program = forms.CharField(label="Program", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    system = forms.ModelChoiceField(label="System", queryset=CurriculumSystem.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    course = forms.ModelChoiceField(label="Course", queryset=Course.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    class_progression_mean_grade_score = forms.CharField(label="Class Progression Mean Grade Score", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    class_capacity = forms.IntegerField(label="Class Capacity", widget=forms.NumberInput(attrs={"class": "form-control"}), required=False)
    students_teacher_ratio = forms.IntegerField(label="Students Teacher Ratio", widget=forms.NumberInput(attrs={"class": "form-control"}), required=False)
    assigned_class_capacity = forms.IntegerField(label="Assigned Class Capacity", widget=forms.NumberInput(attrs={"class": "form-control"}), required=False)
    number_of_streams = forms.IntegerField(label="Number of Streams", widget=forms.NumberInput(attrs={"class": "form-control"}), required=False)
    compulsory_classes = forms.ModelChoiceField(label="Compulsory Classes", queryset=ClusterClass.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    notes = forms.CharField(label="Notes", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    
    class Meta:
        model = GradeLevel
        fields = '__all__'