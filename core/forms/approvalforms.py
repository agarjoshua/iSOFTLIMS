from django import forms
from academics.models import Course
from core.models import DeferrmentApprovalWorklow, Students, TemporaryWithdrawalApprovalWorklow, InterFacultyTransferApprovalWorklow

class AdminDefferementApprovalWorkflowForm(forms.ModelForm):

    admissions_comments = forms.CharField(label="Comments", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    
    class Meta:
        model = DeferrmentApprovalWorklow
        fields = [
            'admissions_comments',
            ]


class TemporaryDefferementApprovalWorkflowForm(forms.ModelForm):

    admissions_comments = forms.CharField(label="Comments", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    
    class Meta:
        model = TemporaryWithdrawalApprovalWorklow
        fields = [
            'admissions_comments',
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
        fields = ['applicant', 'reason', 'current_course', 'desired_course', 'admissions_approved', 'admissions_comments', 'dean_approved', 'dean_comments', 'registrar_approved', 'registrar_comments', 'dvc_approved', 'dvc_comments']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['applicant'].queryset = Students.objects.all()
        self.fields['current_course'].queryset = Course.objects.all()
        self.fields['desired_course'].queryset = Course.objects.all()
    
# class StudentInterFacultyTransferForm(forms.ModelForm):
#     class Meta:
#         model = InterFacultyTransferApprovalWorklow

#         fields = ['applicant','reason','current_course', 'desired_course', 'reason', 'admissions_comments', 'dean_comments', 'registrar_comments', 'dvc_comments']
        
#         widgets = {
#             'applicant': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'} ),
#             'current_course': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
#             # get all courses to enable selection
            
#             'desired_course': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
#             'reason': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
#             'admissions_approved': forms.CheckboxInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
#             'admissions_comments': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
#             'dean_approved': forms.CheckboxInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
#             'dean_comments': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
#             'registrar_approved': forms.CheckboxInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
#             'registrar_comments': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
#             'dvc_comments': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
#         }

class StudentInterFacultyTransferForm(forms.ModelForm):
    # class Meta:
    #     model = InterFacultyTransferApprovalWorklow
    #     fields = ['applicant', 'reason', 'current_course', 'desired_course', 'admissions_approved', 'admissions_comments', 'dean_approved', 'dean_comments', 'registrar_approved', 'registrar_comments', 'dvc_approved', 'dvc_comments']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['applicant'].queryset = Students.objects.all()
    #     self.fields['current_course'].queryset = Course.objects.all()

    #     # Get the selected course if any
    #     selected_course = self.instance.desired_course or None

    #     # Set up the desired_course field as a dropdown with the selected course as the default
    #     self.fields['desired_course'].queryset = Course.objects.all()
    #     self.fields['desired_course'].initial = selected_course
    #     self.fields['desired_course'].widget.attrs.update({'class': 'form-control'})  
    applicant = forms.ModelChoiceField(queryset=Students.objects.all(), label="Applicant", widget=forms.Select(attrs={"class": "form-control"}))
    reason = forms.CharField(label="Reason", max_length=255, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    current_course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Current Course", widget=forms.Select(attrs={"class": "form-control"}))
    desired_course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Desired Course", widget=forms.Select(attrs={"class": "form-control"}))
    admissions_approved = forms.BooleanField(initial=False, required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    admissions_comments = forms.CharField(label="Admissions Comments", max_length=255, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    dean_approved = forms.BooleanField(initial=False, required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    dean_comments = forms.CharField(label="Dean Comments", max_length=255, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    registrar_approved = forms.BooleanField(initial=False, required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    registrar_comments = forms.CharField(label="Registrar Comments", max_length=255, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    dvc_approved = forms.BooleanField(initial=False, required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    dvc_comments = forms.CharField(label="DVC Comments", max_length=255, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = InterFacultyTransferApprovalWorklow
        fields = '__all__'



class StudentSchoolTransferForm(forms.ModelForm):
    class Meta:
        model = InterFacultyTransferApprovalWorklow
        # desired_course = forms.ModelChoiceField(label="Desired Course", queryset=Course.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))
        # desired_course = forms.ModelChoiceField(
        #     label="Desired Course",
        #     queryset=Course.objects.all(),
        #     widget=forms.Select(attrs={"class": "form-control"}),
        #     # initial=user.desired_course  # Set the initial value
        # )

        fields = ['applicant','reason','current_course', 'desired_course', 'reason', 'admissions_comments', 'dean_comments', 'registrar_comments', 'dvc_comments']
        
        widgets = {
            'applicant': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'} ),
            'current_school': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            # get all courses to enable selection
            
            'desired _school': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'reason': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'admissions_approved': forms.CheckboxInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'admissions_comments': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'dean_approved': forms.CheckboxInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'dean_comments': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'registrar_approved': forms.CheckboxInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'registrar_comments': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'dvc_comments': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
        }