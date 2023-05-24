from django import forms
from academics.models import Course
from core.models import DeferrmentApprovalWorklow, TemporaryWithdrawalApprovalWorklow

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