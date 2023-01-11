from django import forms
from core.models import HOD, Staff

class DateInput(forms.DateInput):
    input_type = "date"

class AddDepartmentForm(forms.Form):

    try:
        hod_obj = HOD.objects.all()
        hods = []
        for hod in hod_obj:
            single_hod = hod.id, f"{str(hod.admin.first_name)} {str(hod.admin.last_name)}"
            hods.append(single_hod)

    except Exception:
        hods = []

    try:
        staff_obj = Staff.objects.all()
        staffs = []
        for staff in staff_obj:
            single_staff = staff.id, f"{str(staff.admin.first_name)} {str(staff.admin.last_name)}"
            staffs.append(single_staff)

    except Exception:
        staffs = []

    institution_code = forms.CharField(label="Institution Code", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    name = forms.CharField(label="Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    desc = forms.EmailField(label="Description", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    head = forms.ChoiceField(label="Head of Department", choices=hods, widget=forms.Select(attrs={"class":"form-control"}))
    deputy = forms.ChoiceField(label="Deputy Head of Department", choices=staffs, widget=forms.Select(attrs={"class":"form-control"}))


# class EditHodForm(forms.Form):
#     first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
#     last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
#     email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
#     username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
#     gender_list = (
#         ('Male','Male'),
#         ('Female','Female')
#     )
#     phonenumber = forms.CharField(label="Phone Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))