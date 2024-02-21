from django import forms
from academics.models import Course
from core.models import (
    DeferrmentApprovalWorklow,
    InterSchoolTransferApprovalWorklow,
    School,
    Students,
    TemporaryWithdrawalApprovalWorklow,
    InterFacultyTransferApprovalWorklow,
)


class AdminDefferementApprovalWorkflowForm(forms.ModelForm):

    admissions_comments = forms.CharField(
        label="Comments",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = DeferrmentApprovalWorklow
        fields = [
            "admissions_comments",
        ]


class TemporaryDefferementApprovalWorkflowForm(forms.ModelForm):

    admissions_comments = forms.CharField(
        label="Comments",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = TemporaryWithdrawalApprovalWorklow
        fields = [
            "admissions_comments",
        ]


class InterFacultyTransferWorkflowForm(forms.ModelForm):

    # reason = forms.CharField(label="Comments", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    # # current_course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Current Course", widget=forms.Select(attrs={"class":"form-control"}))
    # # desired_course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Desired Course", widget=forms.Select(attrs={"class":"form-control"}))
    # class Meta:
    #     model = TemporaryWithdrawalApprovalWorklow
    #     fields = [
    #         'admissions_comments',
    #         # 'current_course',
    #         # 'desired_course'
    #         ]
    class Meta:
        model = InterFacultyTransferApprovalWorklow
        fields = [
            "applicant",
            "reason",
            "current_course",
            "desired_course",
            "admissions_approved",
            "admissions_comments",
            "dean_approved",
            "dean_comments",
            "registrar_approved",
            "registrar_comments",
            "dvc_approved",
            "dvc_comments",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["applicant"].queryset = Students.objects.all()
        self.fields["current_course"].queryset = Course.objects.all()
        self.fields["desired_course"].queryset = Course.objects.all()


class StudentInterFacultyTransferForm(forms.ModelForm):
    applicant = forms.ModelChoiceField(
        queryset=Students.objects.all(),
        label="Applicant",
        widget=forms.Select(attrs={"class": "form-control", "readonly": "readonly"}),
    )
    reason = forms.CharField(
        label="Reason",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    current_course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        label="Current Course",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    desired_course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        label="Desired Course",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    admissions_approved = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input mx-3", 
                "disabled": "disabled"
                }
        ),
    )
    admissions_comments = forms.CharField(
        label="Admissions Comments",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
                "class": "form-control", 
                "disabled": "disabled"
                }),
    )
    dean_approved = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
                "class": "form-check-input mx-3", 
                "disabled": "disabled"
                }),
    )
    dean_comments = forms.CharField(
        label="Dean Comments",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
                "class": "form-control", 
                "disabled": "disabled"
                }),
    )
    registrar_approved = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
                "class": "form-check-input mx-3", 
                "disabled": "disabled"
                }),
    )
    registrar_comments = forms.CharField(
        label="Registrar Comments",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
                "class": "form-control", 
                "disabled": "disabled"
                }),
    )
    dvc_approved = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
                "class": "form-check-input mx-3", 
                "disabled": "disabled"
                }),
    )
    dvc_comments = forms.CharField(
        label="DVC Comments",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
                "class": "form-control", 
                "disabled": "disabled"
                }),
    )

    class Meta:
        model = InterFacultyTransferApprovalWorklow
        fields = "__all__"


class StudentSchoolTransferForm(forms.ModelForm):

    applicant = forms.ModelChoiceField(
        queryset=Students.objects.all(),
        label="Applicant",
        widget=forms.Select(attrs={"class": "form-control", "readonly": "readonly"}),
    )
    reason = forms.CharField(
        label="Reason",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    current_school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        label="Current School",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    desired_school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        label="Desired School",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    admissions_approved = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input mx-3", 
                "disabled": "disabled"
                }
        ),
    )
    admissions_comments = forms.CharField(
        label="Admissions Comments",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
                "class": "form-control", 
                "disabled": "disabled"
                }),
    )
    dean_approved = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
                "class": "form-check-input mx-3", 
                "disabled": "disabled"
                }),
    )
    dean_comments = forms.CharField(
        label="Dean Comments",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
                "class": "form-control", 
                "disabled": "disabled"
                }),
    )
    registrar_approved = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
                "class": "form-check-input mx-3", 
                "disabled": "disabled"
                }),
    )
    registrar_comments = forms.CharField(
        label="Registrar Comments",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
                "class": "form-control", 
                "disabled": "disabled"
                }),
    )
    dvc_approved = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
                "class": "form-check-input mx-3", 
                "disabled": "disabled"
                }),
    )
    dvc_comments = forms.CharField(
        label="DVC Comments",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
                "class": "form-control", 
                "disabled": "disabled"
                }),
    )
    class Meta:
        model = InterSchoolTransferApprovalWorklow
        fields = "__all__"
        

        
