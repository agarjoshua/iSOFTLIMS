import json
from django import forms
from core.models import Institution
class InstitutionForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    COUNTRY_CHOICES = [
        ("AF", "Afghanistan"),
        ("AX", "Åland Islands"),
        ("AL", "Albania"),
        ("DZ", "Algeria"),
        ("AS", "American Samoa"),
        ("AD", "Andorra"),
        ("AO", "Angola"),
        ("AI", "Anguilla"),
        ("AQ", "Antarctica"),
        ("AG", "Antigua and Barbuda"),
        ("AR", "Argentina"),
        ("AM", "Armenia"),
        ("AW", "Aruba"),
        ("AU", "Australia"),
        ("AT", "Austria"),
        ("AZ", "Azerbaijan"),
        ("BS", "Bahamas"),
        ("BH", "Bahrain"),
        ("BD", "Bangladesh"),
        ("BB", "Barbados"),
        ("BY", "Belarus"),
        ("BE", "Belgium"),
        ("BZ", "Belize"),
        ("BJ", "Benin"),
        ("BM", "Bermuda"),
        ("BT", "Bhutan"),
        ("BO", "Bolivia"),
        ("BQ", "Bonaire, Sint Eustatius and Saba"),
        ("BA", "Bosnia and Herzegovina"),
        ("BW", "Botswana"),
        ("BV", "Bouvet Island"),
        ("BR", "Brazil"),
        ("IO", "British Indian Ocean Territory"),
        ("BN", "Brunei Darussalam"),
        ("BG", "Bulgaria"),
        ("BF", "Burkina Faso"),
        ("BI", "Burundi"),
        ("CV", "Cabo Verde"),
        ("KH", "Cambodia"),
        ("CM", "Cameroon"),
        ("CA", "Canada"),
        ("KY", "Cayman Islands"),
        ("CF", "Central African Republic"),
        ("TD", "Chad"),
        ("CL", "Chile"),
        ("CN", "China"),
        ("CX", "Christmas Island"),
        ("CC", "Cocos (Keeling) Islands"),
        ("CO", "Colombia"),
        ("KM", "Comoros"),
        ("CG", "Congo"),
        ("CD", "Congo, Democratic Republic of the"),
        ("CK", "Cook Islands"),
        ("CR", "Costa Rica"),
        ("CI", "Côte d'Ivoire"),
        ("HR", "Croatia"),
        ("CU", "Cuba"),
        ("CW", "Curaçao"),
        ("CY", "Cyprus"),
        ("CZ", "Czech Republic"),
        ("DK", "Denmark"),
        ("DJ", "Djibouti"),
        ("DM", "Dominica"),
        ("DO", "Dominican Republic"),
        ("EC", "Ecuador"),
        ("EG", "Egypt"),
        ("SV", "El Salvador"),
        ("GQ", "Equatorial Guinea"),
        ("ER", "Eritrea"),
        ("EE", "Estonia"),
        ("SZ", "Eswatini"),
        ("ET", "Ethiopia"),
        ("FK", "Falkland Islands (Malvinas)"),
        ("FO", "Faroe Islands"),
        ("FJ", "Fiji"),
        ("FI", "Finland"),
        ("FR", "France"),
        ("GF", "French Guiana"),
        ("PF", "French Polynesia"),
        ("TF", "French Southern Territories"),
        ("GA", "Gabon"),
        ("GM", "Gambia"),
        ("GE", "Georgia"),
        ("DE", "Germany"),
        ("GH", "Ghana"),
        ("GI", "Gibraltar"),
        ("GR", "Greece"),
        ("GL", "Greenland"),
        ("GD", "Grenada"),
        ("GP", "Guadeloupe"),
        ("GU", "Guam"),
        ("GT", "Guatemala"),
        ("GG", "Guernsey"),
        ("GN", "Guinea"),
        ("GW", "Guinea-Bissau"),
        ("GY", "Guyana"),
        ("HT", "Haiti"),
        ("HM", "Heard Island and McDonald Islands"),
        ("VA", "Holy See"),
        ("HN", "Honduras"),
        ("HK", "Hong Kong"),
        ("HU", "Hungary"),
        ("IS", "Iceland"),
        ("IN", "India"),
        ("ID", "Indonesia"),
        ("IR", "Iran"),
        ("IQ", "Iraq"),
        ("IE", "Ireland"),
        ("IM", "Isle of Man"),
        ("IL", "Israel"),
        ("IT", "Italy"),
        ("JM", "Jamaica"),
        ("JP", "Japan"),
        ("JE", "Jersey"),
        ("JO", "Jordan"),
        ("KZ", "Kazakhstan"),
        ("KE", "Kenya"),
        ("KI", "Kiribati"),
        ("KP", "North Korea"),
        ("KR", "South Korea"),
        ("KW", "Kuwait"),
        ("KG", "Kyrgyzstan"),
        ("LA", "Laos"),
        ("LV", "Latvia"),
        ("LB", "Lebanon"),
        ("LS", "Lesotho"),
        ("LR", "Liberia"),
        ("LY", "Libya"),
        ("LI", "Liechtenstein"),
        ("LT", "Lithuania"),
        ("LU", "Luxembourg"),
        ("MO", "Macao"),
        ("MG", "Madagascar"),
        ("MW", "Malawi"),
        ("MY", "Malaysia"),
        ("MV", "Maldives"),
        ("ML", "Mali"),
        ("MT", "Malta"),
        ("MH", "Marshall Islands"),
        ("MQ", "Martinique"),
        ("MR", "Mauritania"),
        ("MU", "Mauritius"),
        ("YT", "Mayotte"),
        ("MX", "Mexico"),
        ("FM", "Micronesia"),
        ("MD", "Moldova"),
        ("MC", "Monaco"),
        ("MN", "Mongolia"),
        ("ME", "Montenegro"),
        ("MS", "Montserrat"),
        ("MA", "Morocco"),
        ("MZ", "Mozambique"),
        ("MM", "Myanmar"),
        ("NA", "Namibia"),
        ("NR", "Nauru"),
        ("NP", "Nepal"),
        ("NL", "Netherlands"),
        ("NC", "New Caledonia"),
        ("NZ", "New Zealand"),
        ("NI", "Nicaragua"),
        ("NE", "Niger"),
        ("NG", "Nigeria"),
        ("NU", "Niue"),
        ("NF", "Norfolk Island"),
        ("MK", "North Macedonia"),
        ("MP", "Northern Mariana Islands"),
        ("NO", "Norway"),
        ("OM", "Oman"),
        ("PK", "Pakistan"),
        ("PW", "Palau"),
        ("PS", "Palestine"),
        ("PA", "Panama"),
        ("PG", "Papua New Guinea"),
        ("PY", "Paraguay"),
        ("PE", "Peru"),
        ("PH", "Philippines"),
        ("PN", "Pitcairn"),
        ("PL", "Poland"),
        ("PT", "Portugal"),
        ("PR", "Puerto Rico"),
        ("QA", "Qatar"),
        ("RE", "Réunion"),
        ("RO", "Romania"),
        ("RU", "Russia"),
        ("RW", "Rwanda"),
        ("BL", "Saint Barthélemy"),
        ("SH", "Saint Helena, Ascension and Tristan da Cunha"),
        ("KN", "Saint Kitts and Nevis"),
        ("LC", "Saint Lucia"),
        ("MF", "Saint Martin (French part)"),
        ("PM", "Saint Pierre and Miquelon"),
        ("VC", "Saint Vincent and the Grenadines"),
        ("WS", "Samoa"),
        ("SM", "San Marino"),
        ("ST", "Sao Tome and Principe"),
        ("SA", "Saudi Arabia"),
        ("SN", "Senegal"),
        ("RS", "Serbia"),
        ("SC", "Seychelles"),
        ("SL", "Sierra Leone"),
        ("SG", "Singapore"),
        ("SX", "Sint Maarten (Dutch part)"),
        ("SK", "Slovakia"),
        ("SI", "Slovenia"),
        ("SB", "Solomon Islands"),
        ("SO", "Somalia"),
        ("ZA", "South Africa"),
        ("GS", "South Georgia and the South Sandwich Islands"),
        ("SS", "South Sudan"),
        ("ES", "Spain"),
        ("LK", "Sri Lanka"),
        ("SD", "Sudan"),
        ("SR", "Suriname"),
        ("SJ", "Svalbard and Jan Mayen"),
        ("SE", "Sweden"),
        ("CH", "Switzerland"),
        ("SY", "Syria"),
        ("TW", "Taiwan"),
        ("TJ", "Tajikistan"),
        ("TZ", "Tanzania"),
        ("TH", "Thailand"),
        ("TL", "Timor-Leste"),
        ("TG", "Togo"),
        ("TK", "Tokelau"),
        ("TO", "Tonga"),
        ("TT", "Trinidad and Tobago"),
        ("TN", "Tunisia"),
        ("TR", "Turkey"),
        ("TM", "Turkmenistan"),
        ("TC", "Turks and Caicos Islands"),
        ("TV", "Tuvalu"),
        ("UG", "Uganda"),
        ("UA", "Ukraine"),
        ("AE", "United Arab Emirates"),
        ("GB", "United Kingdom"),
        ("US", "United States"),
        ("UM", "United States Minor Outlying Islands"),
        ("UY", "Uruguay"),
        ("UZ", "Uzbekistan"),
        ("VU", "Vanuatu"),
        ("VE", "Venezuela"),
        ("VN", "Vietnam"),
        ("VG", "Virgin Islands, British"),
        ("VI", "Virgin Islands, U.S."),
        ("WF", "Wallis and Futuna"),
        ("EH", "Western Sahara"),
        ("YE", "Yemen"),
        ("ZM", "Zambia"),
        ("ZW", "Zimbabwe"),
    ]

    country = forms.ChoiceField(label="Country", choices=COUNTRY_CHOICES, widget=forms.Select(attrs={"class": "form-control"}))
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


    institution_location_hierarchy = forms.CharField(label="Location",widget=forms.TextInput(attrs={"class": "form-control"}))

    
    INSTITUTION_CLUSTER = [
        (1, "International"),
        (2, "National"),
        (3, "Extra County"),
        (4, "Sub County"),
        (5, "None"),
    ]
    institution_cluster = forms.MultipleChoiceField(choices=INSTITUTION_CLUSTER, widget=forms.CheckboxSelectMultiple,)
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
    institution_accomodation_type = forms.MultipleChoiceField(choices=INSTITUTION_ACCOMODATION_TYPE, widget=forms.CheckboxSelectMultiple) # type: ignore
    INSTITUTION_STATUS = [(1, "Public"), (2, "Private")]
    institution_status = forms.MultipleChoiceField(choices=INSTITUTION_STATUS, widget=forms.CheckboxSelectMultiple)
    INSTITUTION_TYPE = [(1, "Formal"), (2, "Informal")]
    institution_type = forms.MultipleChoiceField(choices=INSTITUTION_TYPE, widget=forms.CheckboxSelectMultiple)
    institution_in_ASAL_area = forms.BooleanField()
    INSTITUTION_RESIDENCE = [(1, "Rural"), (2, "Urban")]
    institution_residence = forms.MultipleChoiceField(choices=INSTITUTION_RESIDENCE, widget=forms.CheckboxSelectMultiple)
    
    # CONTACT DETAILS
    telephone1 = forms.CharField(label="Telephone 1", widget=forms.TextInput(attrs={"class": "form-control"}))
    telephone2 = forms.CharField(label="Telephone 2", widget=forms.TextInput(attrs={"class": "form-control"}))
    fax_number = forms.CharField(label="Fax Number", widget=forms.TextInput(attrs={"class": "form-control"}))
    email_address = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"class": "form-control"}))
    postal = forms.CharField(label="Postal Address", widget=forms.TextInput(attrs={"class": "form-control"}))
    physical_address1 = forms.CharField(label="Physical Address 1", widget=forms.TextInput(attrs={"class": "form-control"}))
    physical_address2 = forms.CharField(label="Physical Adrress 2", widget=forms.TextInput(attrs={"class": "form-control"}))
    physical_address3 = forms.CharField(label="Physical Address 3", widget=forms.TextInput(attrs={"class": "form-control"}))

    # def contact_details(self):
    #     fields = ['telephone1', 'telephone2', 'fax_number', 'email_address', 'postal', 'physical_address1', 'physical_address2', 'physical_address3']
    #     data = {field: self.cleaned_data[field] for field in fields if self.cleaned_data[field] is not None}
    #     return json.dumps(data)

    #FINANCIAL DETAILS
    bank1 = forms.CharField(label="Bank 1", widget=forms.TextInput(attrs={"class": "form-control"}))
    bank2 = forms.CharField(label="Bank 2", widget=forms.TextInput(attrs={"class": "form-control"}))
    bank3 = forms.CharField(label="Bank 3", widget=forms.TextInput(attrs={"class": "form-control"}))
    bank4 = forms.CharField(label="Bank 4", widget=forms.TextInput(attrs={"class": "form-control"}))
    mobile_money = forms.CharField(label="Mobile Money", widget=forms.TextInput(attrs={"class": "form-control"}))
    pay_bill_number = forms.CharField(label="Paybill Number", widget=forms.TextInput(attrs={"class": "form-control"}))
    till_number = forms.CharField(label="Till Number", widget=forms.TextInput(attrs={"class": "form-control"}))
    pin_number = forms.CharField(label="Pin Number", widget=forms.TextInput(attrs={"class": "form-control"}))
    currency = forms.CharField(label="Currency", widget=forms.TextInput(attrs={"class": "form-control"}))

    # def financial_details(self):
    #     fields = ['bank1', 'bank2', 'bank3', 'bank4', 'mobile_money', 'pay_bill_number', 'till_number', 'pin_number','currency']
    #     data = {field: self.cleaned_data[field] for field in fields if self.cleaned_data[field] is not None}
    #     return json.dumps(data)

    #OTHER STATUTORY DETAILS
    nhif = forms.CharField(label="NHIF", widget=forms.TextInput(attrs={"class": "form-control"}))
    social_security_number = forms.CharField(label="Social Security Number", widget=forms.TextInput(attrs={"class": "form-control"}))
    industrial_training_number = forms.CharField(label="Industrial Training Number", widget=forms.TextInput(attrs={"class": "form-control"}))

    # def other_statutory_details(self):
    #     fields = ['nhif', 'social_security_number', 'industrial_training_number']
    #     data = {field: self.cleaned_data[field] for field in fields if self.cleaned_data[field] is not None}
    #     return json.dumps(data)

    # institution_statutory_numbers = forms.CharField()
    currency = forms.CharField(label="Currency", widget=forms.TextInput(attrs={"class": "form-control"}))


# class InstitutionForm(forms.ModelForm):

#     class Meta:
#         model = Institution
#         fields = '__all__'