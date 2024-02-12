from django import forms
from academics.models import Course
from core.models import DeferrmentApprovalWorklow, TemporaryWithdrawalApprovalWorklow, InterFacultyTransferApprovalWorklow

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

    reason = forms.CharField(label="Comments", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    current_course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Current Course", widget=forms.Select(attrs={"class":"form-control"}))
    desired_course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Desired Course", widget=forms.Select(attrs={"class":"form-control"}))
    class Meta:
        model = TemporaryWithdrawalApprovalWorklow
        fields = [
            'admissions_comments',
            # 'current_course',
            # 'desired_course'
            ]
    
class StudentInterFacultyTransferForm(forms.ModelForm):
    class Meta:
        model = InterFacultyTransferApprovalWorklow
        # desired_course = forms.ModelChoiceField(label="Desired Course", queryset=Course.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))
        desired_course = forms.ModelChoiceField(
            label="Desired Course",
            queryset=Course.objects.all(),
            widget=forms.Select(attrs={"class": "form-control"}),
            # initial=user.desired_course  # Set the initial value
        )

        fields = ['applicant','reason','current_course', 'desired_course', 'reason', 'admissions_comments', 'dean_comments', 'registrar_comments', 'dvc_comments']
        
        widgets = {
            'applicant': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'current_course': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            # get all courses to enable selection
            
            # 'desired_course': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'reason': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'admissions_approved': forms.CheckboxInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'admissions_comments': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'dean_approved': forms.CheckboxInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'dean_comments': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'registrar_approved': forms.CheckboxInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'registrar_comments': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
            'dvc_comments': forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'style': 'background-color: #f8f8f8;'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super(InterFacultyTransferApprovalWorklow, self).__init__(*args, **kwargs)  # noqa: F821
    #     # Prepopulate applicant, current_course, and desired_course fields if instance is provided
    #     instance = kwargs.get('instance')
    #     if instance:
    #         self.fields['applicant'].initial = instance.applicant
    #         self.fields['current_course'].initial = instance.current_course
    #         self.fields['desired_course'].initial = instance.desired_course