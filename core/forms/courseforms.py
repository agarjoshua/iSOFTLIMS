from django import forms
from academics.models import ClusterClass, Course


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'id': 'course_name'})
        }
        
        def clean(self):
            cleaned_data = super().clean() # type: ignore
            if name := cleaned_data.get('name'):
                # Convert the name to upper case
                cleaned_data['name'] = name.upper()
                # Check if a course with the same name already exists
                if Course.objects.filter(name__iexact=name).exists():
                    raise forms.ValidationError('A course with this name already exists.')
            return cleaned_data
        

class CourseEditForm(forms.ModelForm):

    course_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    # compulsory_classes = forms.MultipleChoiceField(, choices=[CHOICES], required=False)
    compulsory_classes = forms.ModelChoiceField(queryset=ClusterClass.objects.all(), label="Compulsory Class", widget=forms.Select(attrs={"class":"form-control"}))
    class Meta:
        model = Course
        fields = ('course_name','compulsory_classes')