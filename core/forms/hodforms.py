from django import forms

from core.models import Department, HODType, StaffType

class DateInput(forms.DateInput):
    input_type = "date"

class AddHodForm(forms.Form):
    hod_type = forms.ModelChoiceField(queryset=HODType.objects.all(), label="Department Head Type", widget=forms.Select(attrs={"class":"form-control"}))
    associated_department = forms.ModelChoiceField(queryset=Department.objects.all(), label="Associated Department", widget=forms.Select(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    phonenumber = forms.CharField(label="Phone Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))


class EditHodForm(forms.Form):
    hod_type = forms.ModelChoiceField(queryset=HODType.objects.all(), label="HOD Type", widget=forms.Select(attrs={"class":"form-control"}))
    associated_department = forms.ModelChoiceField(queryset=Department.objects.all(), label="Associated Department", widget=forms.Select(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    phonenumber = forms.CharField(label="Phone Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))


class AddStaffTypeForm(forms.ModelForm):
    class Meta:
        model = StaffType
        fields = '__all__'