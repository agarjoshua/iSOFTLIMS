from django import forms
from django.forms import Form
from academics.models import GradeLevel, Session
from core.models import Applicant, DeferrmentApprovalWorklow, Students, TemporaryWithdrawalApprovalWorklow
from django.forms import ClearableFileInput
from django.utils.translation import gettext_lazy as _

class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.ModelForm):

    email = forms.EmailField(max_length=200, help_text='Required')
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:

        model = Students
        
        fields = ['email', 'first_name', 'last_name','name', 'registration_number', 'index_number', 'profile_pic', 'address', 'course', 'student_type', 'gender', 'account_status', 'academic_status', 'study_type', 'boarding_type', 'sponsorship_type', 'sponsor_type', 'special_needs', 'require_transport', 'student_contact', 'sponsor_contact'] # type: ignore

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'index_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'student_type': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'account_status': forms.Select(attrs={'class': 'form-control'}),
            'academic_status': forms.Select(attrs={'class': 'form-control'}),
            'study_type': forms.Select(attrs={'class': 'form-control'}),
            'boarding_type': forms.Select(attrs={'class': 'form-control'}),
            'sponsorship_type': forms.Select(attrs={'class': 'form-control'}),
            'sponsor_type': forms.Select(attrs={'class': 'form-control'}),
            'special_needs': forms.Select(attrs={'class': 'form-control'}),
            'require_transport': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # 'student_contact': forms.JSONInput(attrs={'class': 'form-control'}),
            # 'sponsor_contact': forms.JSONInput(attrs={'class': 'form-control'}), 
        }

class AddedStudentForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=50,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Password",
        max_length=50,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        label="Username",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    address = forms.CharField(
        label="Address",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    # For Displaying Session Years
    try:
        session_years = Session.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (
                session_year.id,
                f"{str(session_year.session_start_date)} to {str(session_year.session_end_date)}",
            )

            session_year_list.append(single_session_year)

    except Exception:
        session_year_list = []
    session_year_id = forms.ChoiceField(
        label="Session Year",
        choices=session_year_list,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    gender_list = (("Male", "Male"), ("Female", "Female"))

    gender = forms.ChoiceField(
        label="Gender",
        choices=gender_list,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    session_start_year = forms.DateField(
        label="Session Start", widget=DateInput(attrs={"class": "form-control"})
    )
    session_end_year = forms.DateField(
        label="Session End", widget=DateInput(attrs={"class": "form-control"})
    )
    profile_pic = forms.FileField(
        label="Profile Pic",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )


class EditStudentForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=50,
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        label="Username",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    address = forms.CharField(
        label="Address",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    # For Displaying Session Years
    try:
        session_years = Session.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (
                session_year.id,
                f"{str(session_year.session_start_date)} to {str(session_year.session_end_date)}",
            )

            session_year_list.append(single_session_year)

    except Exception:
        session_year_list = []

    gender_list = (("Male", "Male"), ("Female", "Female"))

    gender = forms.ChoiceField(
        label="Gender",
        choices=gender_list,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    session_year_id = forms.ChoiceField(
        label="Session Year",
        choices=session_year_list,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    profile_pic = forms.FileField(
        label="Profile Pic",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )


class DefferementApprovalWorkflowForm(forms.ModelForm):

    reason = forms.CharField(label="Reason for deferement", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model = DeferrmentApprovalWorklow
        fields = ['reason']

class TemporaryWithdrawalApprovalWorklowForm(forms.ModelForm):

    reason = forms.CharField(label="Reason for temporary withdrawal", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model = TemporaryWithdrawalApprovalWorklow
        fields = ['reason']