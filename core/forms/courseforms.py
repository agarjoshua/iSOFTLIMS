from django import forms
from academics.models import Course


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