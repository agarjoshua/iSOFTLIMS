from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator

# from django_countries.fields import *
from django.forms import MultipleChoiceField


# from academics.models import Grade, Session
"""


"""
# Create your models here.
class Institution(models.Model):
    id = models.AutoField(primary_key=True)
    institution_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=30)
    country = CountryField(blank_label="(select country)", null=True)
    INSTITUTION_ORDER = [
        (1, "University"),
        (2, "College"),
        (3, "Advanced Level"),
        (4, "Secondary"),
        (4, "Primary"),
        (4, "Pre-Primary"),
        (5, "Kindergarten"),
    ]
    institution_order = models.TextField()
    registration_date = models.DateTimeField(auto_now=True, editable=False)
    examination_centre_number = models.CharField(max_length=12, null=True)
    institution_location_hierarchy = models.TextField()
    CLUSTER = [
        (1, "International"),
        (2, "National"),
        (3, "Extra County"),
        (4, "Sub County"),
        (5, "None"),
    ]
    institution_cluster = models.TextField()
    CATEGORY = [
        (1, "Ordinary"),
        (2, "Integrated"),
        (3, "Special"),
        (4, "Mobile"),
        (5, "Online"),
        (6, "None"),
    ]
    institution_category = models.TextField()
    GENDER = [
        (1, "Mixed"),
        (2, "Boys Only"),
        (3, "Girls Only"),
    ]
    institution_gender_category = models.TextField()
    ACCOMODATION = [
        (1, "All"),
        (2, "Day Only"),
        (3, "Boarders Only"),
    ]
    institution_accomodation_type = models.TextField()
    STATUS = [(1, "Public"), (2, "Private")]
    institution_status = models.CharField(max_length=255, choices=STATUS, default="1")
    TYPE = [(1, "Formal"), (2, "Informal")]
    institution_type = models.CharField(
        max_length=255, choices=TYPE, default="1", null=False
    )
    institution_in_ASAL_area = models.BooleanField(null=False, default=False)
    RESIDENCE = [(1, "Rural"), (2, "Urban")]
    institution_residence = models.TextField()
    contact_details = models.JSONField(null=True)
    institution_statutory_numbers = models.JSONField(null=True)
    # Use Base currency or Other Currency?
    currency = models.CharField(max_length=20, null=True)
    bank_details = models.JSONField(null=True)
    # TODO: Nationalities & Currencies (List World Nationalities & their Currencies & provide capture of exchange rate against Base currency)
    logo = models.FileField(null=True)
    objects = models.Manager()


class Campus(models.Model):
    id = models.AutoField(primary_key=True)
    institution_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    campus_code = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=30)
    physical_address = models.CharField(max_length=255, null=True)
    notes = models.TextField(null=True)
    gl_account = models.CharField(max_length=255, null=True)
    STATUS = [(1, "Active"), (2, "Inactive")]
    status = models.CharField(max_length=255, choices=STATUS, default="1")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
    # class Meta:
    #     ordering = ['id']

    def get_next(self):
        return Campus.objects.filter(id__gt=self.id).order_by('id').first()
    
    def get_previous(self):
        return Campus.objects.filter(id__lt=self.id).order_by('-id').first()
    
    def get_first(self):
        return Campus.objects.order_by('id').first()

    def get_last(self):
        return Campus.objects.order_by('id').last()
    

class School(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    campus = models.ForeignKey(Campus, on_delete=models.DO_NOTHING, null=True)
    gl_account = models.CharField(max_length=255, null=True)
    notes = models.TextField(null=True)
    STATUS = [(1, "Active"), (2, "Inactive")]
    status = models.CharField(max_length=255, choices=STATUS, default="1")
    objects = models.Manager()

    def __str__(self):
        return self.name


class Program(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=30)
    duration = models.CharField(max_length=30)
    number_of_terms = models.CharField(max_length=30)
    current_term = models.CharField(max_length=30)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, null=True)
    minimum_examinable_subjects = models.CharField(max_length=30)
    maximum_examinable_subjects = models.CharField(max_length=30)
    final_exam_marks_based_on = models.CharField(max_length=30)
    mean_mark_to_advance_to_next_level = models.CharField(max_length=30)
    curriculum_description = models.CharField(max_length=30)
    class_progression = models.CharField(max_length=30)
    progression_next_level = models.CharField(max_length=30)
    gl_account = models.CharField(max_length=30)
    notes = models.TextField(null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    duration = models.CharField(max_length=30)
    number_of_terms = models.CharField(max_length=30)
    current_term = models.CharField(max_length=30)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, null=True)
    minimum_examinable_subjects = models.CharField(max_length=30)
    maximum_examinable_subjects = models.CharField(max_length=30)
    final_exam_marks_based_on = models.CharField(max_length=30)
    mean_mark_to_advance_to_next_level = models.CharField(max_length=30)
    curriculum_description = models.CharField(max_length=30)
    class_progression = models.CharField(max_length=30)
    progression_next_level = models.CharField(max_length=30)
    gl_account = models.CharField(max_length=30)
    notes = models.TextField(null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
    



class CurriculumSystem(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    study_period = models.CharField(max_length=30)
    levels = models.CharField(max_length=30)
    campuses = models.CharField(max_length=30)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, null=True)
    gl_account = models.CharField(max_length=30)
    notes = models.TextField(null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    user_type_data = (
        (1, "Admin"),
        (2, "Staff"),
        (3, "Student"),
        (4, "HOD"),
        (5, "Guardian"),
        (6, "Teacher"),
        (7, "Specialuser"),
        (8, "Applicant")
    )
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    login_attempts = models.PositiveIntegerField(default=0)
    cooldown_end_time = models.DateTimeField(null=True, blank=True)
    user_account_status = (
        ("Suspended", "Suspended"),
        ("Deactivated", "Deactivated"),
        ("Activation Requested", "Activation Requested"),
        ("Active", "Active"),
    )
    account_status = models.CharField(default="Active", choices=user_account_status, max_length=20)

    class Meta:
        ordering = ['id']

    def get_user_type(self):
        for user_type in self.user_type_data:
            if str(self.user_type) == str(user_type[0]):
                return user_type[1]
        return None


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(null=True)
    admin_type = models.ForeignKey('AdminType', on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.admin.first_name}  {self.admin.last_name}"

class AdminType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=12, null=True, unique=True)
    objects = models.Manager()

class HOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING)
    hod_type = models.ForeignKey('HODType', on_delete=models.DO_NOTHING, null=True)
    associated_department = models.ForeignKey('Department', on_delete=models.DO_NOTHING, null=True)
    CONTRACT_TYPE = [
        (1, "Permanent"),
        (2, "Long Term"),
        (3, "Short Term"),
        (4, "Contracted Labour"),
        (5, "Probation"),
    ]
    contract_type = models.CharField(default=5, choices=CONTRACT_TYPE, max_length=50)
    phonenumber = models.CharField(max_length=12)
    # institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.admin.first_name}  {self.admin.last_name}"
    

class HODType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=12, null=True, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,default='Teacher')
    phonenumber = models.CharField(max_length=12, null=True)
    secondary_phone_number = models.CharField(max_length=12, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    pin_tax_number = models.CharField(max_length=12, null=True)
    nhif = models.CharField(max_length=12, null=True)
    social_security_number = models.CharField(max_length=12, null=True)
    industrial_training_number = models.CharField(max_length=12, null=True)
    statutory_numbers = models.JSONField(null=True)
    bank_account = models.CharField(max_length=12, null=True)
    secondary_bank_account = models.CharField(max_length=12, null=True)
    bank_details = models.JSONField(null=True)
    CONTRACT_TYPE = [
        (1, "Permanent"),
        (2, "Long Term"),
        (3, "Short Term"),
        (4, "Contracted Labour"),
        (5, "Probation"),
    ]
    contract_type = models.CharField(default=5, choices=CONTRACT_TYPE, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.admin.first_name}  {self.admin.last_name}"

class StaffType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True)

class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    associated_department = models.ForeignKey('Department', on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=255,null=True)
    address = models.TextField()
    telephone = models.CharField(max_length=255,null=True)
    email = models.EmailField(null=True)
    staff_type = models.ForeignKey(StaffType, blank=True, null=True, on_delete=models.DO_NOTHING) # type: ignore
    CONTRACT_TYPE = [
        (1, "Permanent"),
        (2, "Long Term"),
        (3, "Short Term"),
        (4, "Contracted Labour"),
        (5, "Probation"),
    ]
    contract_type = models.CharField(default=5, choices=CONTRACT_TYPE, max_length=50) # type: ignore
    description = models.CharField(max_length=255, null=True)
    contract_years = models.CharField(max_length=255, default="Parmanent")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.admin.first_name}  {self.admin.last_name}"



class Department(models.Model):
    id = models.AutoField(primary_key=True)
    campus = models.ForeignKey(Campus, on_delete=models.DO_NOTHING, null=True)
    gl_account = models.CharField(max_length=255, null=True)
    notes = models.TextField(null=True)
    code = models.CharField(max_length=30, null=True)
    institution_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    department_code = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255, default="institution", null=True)
    head = models.ForeignKey(HOD, on_delete=models.DO_NOTHING, null=True)
    deputy = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    status = models.BooleanField(default=True)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, null=True)


    def __str__(self):
        return self.name
    
    # class Meta:
    #     ordering = ['id']

    def get_next(self):
        return Department.objects.filter(id__gt=self.id).order_by('id').first()
    
    def get_previous(self):
        return Department.objects.filter(id__lt=self.id).order_by('-id').first()
    
    def get_first(self):
        return Department.objects.order_by('id').first()

    def get_last(self):
        return Department.objects.order_by('id').last()


class Guardian(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING)
    phonenumber = models.CharField(max_length=12)
    bank = models.CharField(null=True, max_length=2550)
    gender = models.CharField(max_length=50)

    def __str__(self):
        return self.user.name


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, null=True)
    admission_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255,null=True)
    registration_number = models.CharField(max_length=10, unique=True, null=True)
    index_number = models.CharField(max_length=20, unique=True, null=True)
    profile_pic = models.FileField(null=True)
    address = models.TextField(null=True)
    course = models.ForeignKey("academics.Course", on_delete=models.DO_NOTHING, null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True)
    # grade = models.ForeignKey('academics.Gradelevel', on_delete=models.DO_NOTHING, null=True)
    STUDENT_TYPE = [
        ("1", "Local"), 
        ("2", "International")]
    student_type = models.CharField(max_length=10, choices=STUDENT_TYPE, default="1")
    GENDER = [
        ("1", "Male"), 
        ("2", "Female")]
    gender = models.CharField(max_length=10, choices=GENDER, default="1")
    ACCOUNT_STATUS = [
        ("1", "Active"),
        ("2", "Inactive"),
        ("3", "On-Hold"),
        ("4", "Suspended"),
        ("5", "Terminated"),
    ]
    account_status = models.CharField(max_length=10, choices=ACCOUNT_STATUS, default="1")
    ACADEMIC_STATUS = [
        (1, "Active"),
        (2, "Inactive"),
        (3, "On-Hold"),
        (4, "Suspended"),
        (5, "Repeat"),
    ]
    academic_status = models.CharField(
        max_length=10, choices=ACCOUNT_STATUS, default="1"
    )
    STUDENT_STUDY_TYPE = [
        ("1", "Full Time"), 
        ("2", "Part Time"), 
        ("3", "Online")]
    study_type = models.CharField(
        max_length=10, choices=STUDENT_STUDY_TYPE, default="1"
    )
    STUDENT_BOARDING_TYPE = [
        ("1", "Boarder"), 
        ("2", "Day-Scholer")]
    boarding_type = models.CharField(
        max_length=10, choices=STUDENT_BOARDING_TYPE, default="1"
    )
    STUDENT_SPONSORSHIP_TYPE = [
        ("1", "Self-Sponsored"), 
        ("2", "Sponsored")]
    sponsorship_type = models.CharField(
        max_length=10, choices=STUDENT_SPONSORSHIP_TYPE, default="1"
    )
    STUDENT_SPONSOR_TYPE = [
        ("1", "Government"), 
        ("2", "Organizations"), 
        ("3", "Sponsor")]
    sponsor_type = models.CharField(
        max_length=10, choices=STUDENT_SPONSOR_TYPE, default="1"
    )
    STUDENT_SPECIAL_NEEDS_TYPE = [
        ("1", "Physically Impaired"),
        ("2", "Visually Impaired"),
        ("3", "Hearing Impaired"),
        ("4", "Intellectually Impaired"),
        ("5", "Multiple Disabilities"),
        ("6", "Other Impairment"),
    ]
    special_needs = models.CharField(
        max_length=255, choices=STUDENT_SPECIAL_NEEDS_TYPE, default="1"
    )
    require_transport = models.BooleanField(default=False)
    student_contact = models.CharField(max_length=255, unique=True, null=True)
    sponsor_contact = models.CharField(max_length=255, unique=True, null=True)
    booked_hostel = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.name)
    
    
#     a. Registration Type (New/Continuing)
# b. Pupil/Student Type (Local/International)
# c. Gender (Male/Female)
# d. Account Status (Active/Inactive/On-Hold/Suspended/Terminated)
# e. Study Type (Full Time/Part Time/Online)
# f. Boarding Type (Boarder/Day Scholar)
# g. Student Type (Local/Regional/International)
# h. Sponsorship Type (Self-Sponsored/Sponsored)
# i. Sponsors (Government/Organizations/Individuals)
# j. Relationships (Parent/Guardian/Sponsor)
# k. Special Needs (Physically Impaired/Visually Impaired/Hearing
# Impaired/Intellectually Impaired/Multiple Disabilities/Other Impairment)
# l. Nationalities &amp; Currencies (List World Nationalities &amp; their Currencies &amp;
# provide capture of exchange rate against Base currency)
# m. Religions (List Major World Religions)
# n. Extra-Curriculum Activities (Music/Football/Netball/Athletics/Drama)
# o. Require Services (Yes/No)
# p. Entry Exam Required (Yes/No)
# q. Type of Entry Examination (Normal/Government/Special)
# r. Compulsory (Yes/No)
# s. Contract Type (Permanent/Long Term/Short Term/Contracted Labour)
# t. Job Type (Permanent/Contractual/Temporary)
# u. Staff Category (Administrative/Teaching/Support)
# v. Staff Type (Vice Chancellor/Deputy Vice Chancellor/Dean/Head of
# Department/Teacher/Lecturer/Director/Manager/Officer/Employee/Support)
# w. Payment Methods (Cheque/Direct Bank Deposit/EFT-Electronic File
# Transfer/RTGS-Real Time Gross Settlement/Mobile Money/In-Kind)
# x. Payment Reference Required (Yes/No)
# y. Fee Item Categories (Tuition/Other Billable Item)
# z. Fee Item Occurrence (One Off/Variable/Per Semester/Per Academic Year)
# aa. Fee Item Applicability (All Students/Day Scholars Only/Boarders
# Only/International Students Only/Local Students Only/Class/Form/First Year

# iSoft LIMS (iSoft Learning Institution Information Management System) Core Module Brief

# ©iSoft Systems 2023 All Rights Reserved

# Quality Driven Solutions
# Students Only/ Second Year Students Only/ Third Year Students Only/Final Year
# Students Only)
# bb. Fee Item Payment Priority (0-9)
# cc. Services Type (Permanent/Sessional)
# dd. Payment Plan (Pre-Paid/Post-Paid)


#: TODO
## implement the student registration number field properly
# class Student(models.Model):
#     registration_number = models.CharField(max_length=10, unique=True, editable=False, default=generate_registration_number)
#     # other fields ...


def generate_registration_number():
    # code to generate unique registration number
    return "SCHOOL-" + str(uuid.uuid4().int)[:10]


class Applicant(models.Model):
    PROGRAMME_CHOICES = (
        ('PGD', 'Postgraduate Diploma'),
        ('MSc', 'Masters'),
        ('PhD', 'Doctorate'),
    )

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    SPECIAL_NEEDS_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    MODE_OF_STUDY_CHOICES = (
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('EL', 'eLearning'),
    )
    applicant = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING)
    surname = models.CharField(max_length=255,null=True)
    other_names = models.CharField(max_length=255,null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True)
    nationality = models.CharField(max_length=255,null=True)
    id_or_passport_number = models.CharField(max_length=255,null=True)
    date_of_birth = models.DateField(null=True)
    county = models.CharField(max_length=255,null=True)
    telephone = models.CharField(max_length=255,null=True)
    email = models.EmailField(null=True)
    current_address = models.TextField(null=True)
    permanent_address = models.TextField(blank=True,null=True)
    special_needs = models.CharField(max_length=1, choices=SPECIAL_NEEDS_CHOICES,null=True)
    special_needs_description = models.TextField(blank=True)
    programme_level = models.CharField(max_length=3, choices=PROGRAMME_CHOICES,null=True)
    degree_name = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    concept_paper = models.FileField(blank=True)
    masters_degree_type = models.CharField(max_length=255, blank=True)
    masters_degree_title = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True)
    expected_completion_date = models.DateField(null=True)
    mode_of_study = models.CharField(max_length=2, choices=MODE_OF_STUDY_CHOICES,blank=True)
    photo_1 = models.ImageField(null=True)
    photo_2 = models.ImageField(null=True)
    secondary_schools_attended = models.TextField(blank=True)
    university_education = models.TextField(blank=True)
    other_degrees_or_diploma = models.TextField(blank=True)
    research_experience = models.TextField(blank=True)
    employment_work_experience = models.TextField(blank=True)
    languages_spoken = models.TextField(blank=True)
    referee1_name = models.CharField(max_length=255, blank=True)
    referee1_designation = models.CharField(max_length=255, blank=True)
    referee1_address = models.TextField(blank=True)
    referee1_telephone = models.CharField(max_length=255, blank=True)
    referee1_email = models.EmailField(blank=True)
    referee2_name = models.CharField(max_length=255, blank=True)
    referee2_designation = models.CharField(max_length=255, blank=True)
    referee2_address = models.TextField(blank=True)
    referee2_telephone = models.CharField(max_length=255, blank=True)
    referee2_email = models.EmailField(blank=True)
    how_did_you_know_about_us = models.CharField(max_length=255, blank=True)
    require_entry_exams = models.BooleanField(default=True)
    application_status = models.BooleanField(default=False)
    objects = models.Manager()


class ApplicantApprovalWorklow(models.Model):
    id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    finance_approved = models.BooleanField(default=False)
    department_approved = models.BooleanField(default=False)
    dvc_approved = models.BooleanField(default=False)

class DeferrmentApprovalWorklow(models.Model):
    id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(Students, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, blank=True)
    admissions_approved = models.BooleanField(default=False)
    admissions_comments = models.CharField(max_length=255, blank=True)
    dean_approved = models.BooleanField(default=False)
    dean_comments = models.CharField(max_length=255, blank=True)
    registrar_approved = models.BooleanField(default=False)
    registrar_comments = models.CharField(max_length=255, blank=True)
    dvc_approved = models.BooleanField(default=False)
    dvc_comments = models.CharField(max_length=255, blank=True)
    objects = models.Manager()

class TemporaryWithdrawalApprovalWorklow(models.Model):
    id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(Students, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, blank=True)
    admissions_approved = models.BooleanField(default=False)
    admissions_comments = models.CharField(max_length=255, blank=True)
    dean_approved = models.BooleanField(default=False)
    dean_comments = models.CharField(max_length=255, blank=True)
    registrar_approved = models.BooleanField(default=False)
    registrar_comments = models.CharField(max_length=255, blank=True)
    dvc_approved = models.BooleanField(default=False)
    dvc_comments = models.CharField(max_length=255, blank=True)
    objects = models.Manager()

class InterFacultyTransferApprovalWorklow(models.Model):
    id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(Students, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, blank=True)
    current_course = models.ForeignKey("academics.Course", on_delete=models.DO_NOTHING, null=True, blank=True, related_name='current_course_approvals')
    desired_course = models.ForeignKey("academics.Course", on_delete=models.DO_NOTHING, null=True, blank=True, related_name='desired_course_approvals')
    admissions_approved = models.BooleanField(default=False)
    admissions_comments = models.CharField(max_length=255, blank=True, null=True)
    dean_approved = models.BooleanField(default=False, null=True)
    dean_comments = models.CharField(max_length=255, blank=True, null=True)
    registrar_approved = models.BooleanField(default=False, null=True)
    registrar_comments = models.CharField(max_length=255, blank=True, null=True)
    dvc_approved = models.BooleanField(default=False, null=True)
    dvc_comments = models.CharField(max_length=255, blank=True, null=True)
    objects = models.Manager()


class InterSchoolTransferApprovalWorklow(models.Model):
    id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(Students, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, blank=True)
    current_school = models.ForeignKey("core.School", on_delete=models.DO_NOTHING, null=True, related_name='current_school_approvals')
    desired_school = models.ForeignKey("core.School", on_delete=models.DO_NOTHING, null=True, related_name='desired_school_approvals')
    admissions_approved = models.BooleanField(default=False)
    admissions_comments = models.CharField(max_length=255, blank=True)
    dean_approved = models.BooleanField(default=False)
    dean_comments = models.CharField(max_length=255, blank=True)
    registrar_approved = models.BooleanField(default=False)
    registrar_comments = models.CharField(max_length=255, blank=True)
    dvc_approved = models.BooleanField(default=False)
    dvc_comments = models.CharField(max_length=255, blank=True)
    objects = models.Manager()


class SpecialUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=12)

    def __str__(self):
        return self.user.name


class House(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Both', 'Both'),
    ]

    name = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    campus = models.ForeignKey(Campus, on_delete=models.DO_NOTHING, null=True)
    current_capacity = models.IntegerField(default=0)
    maximum_capacity = models.IntegerField(default=0)

    def is_capacity_available(self):
        return self.current_capacity < MAX_CAPACITY
    
    def __str__(self):
        return self.name or 'name'


# Dormitories/Hostels
# Code
# Description
# Gender (Male/Female/Co-Ed)
# Bed Capacity
# Occupied
# Damaged
# Damaged Remarks
# Available
# Minimum Percentage Bed Capacity Warning
# No. of Sections e.g. 2:
# Section Code
# Description
# Bed capacity
# Occupied
# Damaged
# Damaged Remarks
# Available
# No. of cubicles e.g. 10:
# Bed capacity
# No. of cubicles e.g. 4
# Occupied
# Damaged
# Damaged Remarks
# Available



class Booking(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)
    session = models.ForeignKey("academics.Session", on_delete=models.DO_NOTHING, null=True)
    status = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return f'House Name: {self.house.name} Student: {self.student.name}'



class Service(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    service_unit_of_measure = models.CharField(max_length=30)
    rate = models.CharField(max_length=30)
    payment_plan = models.CharField(max_length=30)
    taxable = models.CharField(max_length=30)
    tax_rate = models.CharField(max_length=30)
    gl_account = models.CharField(max_length=30)
    notes = models.TextField(null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class EcActivities(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Both', 'Both'),
    ]
    code = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    campus = models.ForeignKey(Campus, on_delete=models.DO_NOTHING, null=True)


class Job(models.Model):
    code = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    gl_account = models.CharField(max_length=100)
    notes = models.TextField(null=True)
    objects = models.Manager()

    def __str__(self):
        return self.description


class UserResponsibility(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True)
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING, null=True)
    objects = models.Manager()


class DiscplinaryManagement(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True)
    displinary_action = models.CharField(max_length=255)
    discplinary_case_notes = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    resumption_date = models.DateTimeField()
    notes = models.CharField(max_length=255)
    objects = models.Manager()

    def __str__(self):
        return f'Case {self.subject}, Name {self.subject.name}'
    



# Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    def generate_registration_number(school):
        # code to generate unique registration number
        return f"SCHOOL-{school[:5]}{str(uuid.uuid4().int)[:10]}"

    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            Admin.objects.create(
                admin=instance,
                # institution=Institution.objects.get(id=1)
            )
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        # Generate student unique ID number

        if instance.user_type == 3:
            Students.objects.create(
                admin=instance,
                # course_id=Courses.objects.get(id=1),
                # session_year_id=Session.objects.get(id=1),
                address="",
                profile_pic="",
                gender="",
                # registration_number = generate_registration_number(school)
            )
        if instance.user_type == 4:
            HOD.objects.create(admin=instance)
        if instance.user_type == 5:
            Guardian.objects.create(admin=instance)
        if instance.user_type == 6:
            Teacher.objects.create(admin=instance)
        if instance.user_type == 7:
            Guardian.objects.create(admin=instance)
        if instance.user_type == 8:
            Applicant.objects.create(applicant=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.students.save()
    if instance.user_type == 4:
        instance.hod.save()
    if instance.user_type == 5:
        instance.guardian.save()
    if instance.user_type == 6:
        instance.teacher.save()
    if instance.user_type == 7:
        instance.guardian.save()
    if instance.user_type == 8:
        instance.applicant.save()
