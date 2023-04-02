from django import forms
from academics.models import Class, ClusterClass

class ClusterClassForm(forms.ModelForm):
    classes = forms.ModelMultipleChoiceField(queryset=Class.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = ClusterClass
        fields = ['cluster_class_name', 'classes']

    # def save(self, commit=True, force_insert=False):
    #     instance = super().save(commit=False)
    #     if commit:
    #         instance. super().save()
    #         self.save_m2m()
    #     return instance