from django import forms
from core.models import DeferrmentApprovalWorklow

class AdminDefferementApprovalWorkflowForm(forms.ModelForm):

    admissions_comments = forms.CharField(label="Comments", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    # admisions_approved = forms.BooleanField(label='Approve the Defer')
    class Meta:
        model = DeferrmentApprovalWorklow
        fields = [
            'admissions_comments',
            # 'admissions_approved'
            ]

class DeanDefferementApprovalWorkflowForm(forms.ModelForm):

    dean_comments = forms.CharField(label="Comments", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    # dean_approved = forms.BooleanField(label='Approve the Defer')
    class Meta:
        model = DeferrmentApprovalWorklow
        fields = [
            'dean_comments',
            # 'dean_approved'
            ]

class RegistrarDefferementApprovalWorkflowForm(forms.ModelForm):

    registrar_comments = forms.CharField(label="Comments", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    # registrar_approved = forms.BooleanField(label='Approve the Defer')
    class Meta:
        model = DeferrmentApprovalWorklow
        fields = [
            'registrar_comments', 
            # 'registrar_approved'
            ]

class DVCDefferementApprovalWorkflowForm(forms.ModelForm):

    dvc_comments = forms.CharField(label="Comments", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    # dvc_approved = forms.BooleanField(label='Approve the Defer')
    class Meta:
        model = DeferrmentApprovalWorklow
        fields = [
            'dvc_comments',
            # 'dvc_approved'
            ]