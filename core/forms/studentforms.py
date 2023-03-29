from django import forms
from django.forms import Form
from academics.models import Session


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
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
        widget=forms.EmailInput(attrs={"class": "form-control"}),
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

    gender_list = (("Male", "Male"), ("Female", "Female"))

    gender = forms.ChoiceField(
        label="Gender",
        choices=gender_list,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    session_year_id = forms.ChoiceField(
        label="Session Year",
        choices=session_year_list,
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
