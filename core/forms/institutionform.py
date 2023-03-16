import json
from django import forms

class InstitutionForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'school.name'}))
    country = forms.CharField()
    INSTITUTION_ORDER = [
        (1, "University"),
        (2, "College"),
        (3, "Advanced Level"),
        (4, "Secondary"),
        (4, "Primary"),
        (4, "Pre-Primary"),
        (5, "Kindergarten"),
    ]
    institution_order = forms.MultipleChoiceField(choices=INSTITUTION_ORDER, widget=forms.CheckboxSelectMultiple)
    institution_location_hierarchy = forms.CharField()
    INSTITUTION_CLUSTER = [
        (1, "International"),
        (2, "National"),
        (3, "Extra County"),
        (4, "Sub County"),
        (5, "None"),
    ]
    institution_cluster = forms.MultipleChoiceField(choices=INSTITUTION_CLUSTER, widget=forms.CheckboxSelectMultiple)
    INSTITUTION_CATEGORY = [
        (1, "Ordinary"),
        (2, "Integrated"),
        (3, "Special"),
        (4, "Mobile"),
        (5, "Online"),
        (6, "None"),
    ]
    institution_category = forms.MultipleChoiceField(choices=INSTITUTION_CATEGORY, widget=forms.CheckboxSelectMultiple)
    INSTITUTION_GENDER_CATEGORY = [
        (1, "Mixed"),
        (2, "Boys Only"),
        (3, "Girls Only"),
    ]
    institution_gender_category = forms.MultipleChoiceField(choices=INSTITUTION_GENDER_CATEGORY, widget=forms.CheckboxSelectMultiple)
    INSTITUTION_ACCOMODATION_TYPE = [
        (1, "All"),
        (2, "Day Only"),
        (3, "Boarders Only"),
    ]
    institution_accomodation_type = forms.MultipleChoiceField(choices=INSTITUTION_ACCOMODATION_TYPE, widget=forms.CheckboxSelectMultiple)
    INSTITUTION_STATUS = [(1, "Public"), (2, "Private")]
    institution_status = forms.ChoiceField(choices=INSTITUTION_STATUS)
    INSTITUTION_TYPE = [(1, "Formal"), (2, "Informal")]
    institution_type = forms.ChoiceField(choices=INSTITUTION_TYPE)
    institution_in_ASAL_area = forms.BooleanField(required=False)
    INSTITUTION_RESIDENCE = [(1, "Rural"), (2, "Urban")]
    institution_residence = forms.MultipleChoiceField(choices=INSTITUTION_RESIDENCE)
    
    # CONTACT DETAILS
    telephone1 = forms.CharField()
    telephone2 = forms.CharField(required=False)
    fax_number = forms.CharField(required=False)
    email_address = forms.EmailField(required=False)
    postal = forms.CharField()
    physical_address1 = forms.CharField()
    physical_address2 = forms.CharField(required=False)
    physical_address3 = forms.CharField(required=False)

    def contact_details(self):
        fields = ['telephone1', 'telephone2', 'fax_number', 'email_address', 'postal', 'physical_address1', 'physical_address2', 'physical_address3']
        data = {field: self.cleaned_data[field] for field in fields if self.cleaned_data[field] is not None}
        return json.dumps(data)

    #FINANCIAL DETAILS
    bank1 = forms.CharField(required=False)
    bank2 = forms.CharField(required=False)
    bank3 = forms.CharField(required=False)
    bank4 = forms.CharField(required=False)
    mobile_money = forms.CharField(required=False)
    pay_bill_number = forms.CharField(required=False)
    till_number = forms.CharField(required=False)
    pin_number = forms.CharField(required=False)
    currency = forms.CharField(required=False)

    def financial_details(self):
        fields = ['bank1', 'bank2', 'bank3', 'bank4', 'mobile_money', 'pay_bill_number', 'till_number', 'pin_number','currency']
        data = {field: self.cleaned_data[field] for field in fields if self.cleaned_data[field] is not None}
        return json.dumps(data)

    #OTHER STATUTORY DETAILS
    nhif = forms.CharField(required=False)
    social_security_number = forms.CharField(required=False)
    industrial_training_number = forms.CharField(required=False)

    def other_statutory_details(self):
        fields = ['nhif', 'social_security_number', 'industrial_training_number']
        data = {field: self.cleaned_data[field] for field in fields if self.cleaned_data[field] is not None}
        return json.dumps(data)

    institution_statutory_numbers = forms.CharField()
    currency = forms.CharField()