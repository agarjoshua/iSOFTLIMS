from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django_countries.fields import CountryField

# from django_countries.fields import *
from django.forms import MultipleChoiceField


from academics.models import Grade, Session


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
    # TODO: Implement a counties list programme in python (january 25th projects)
    # WRITE ABOUT THE ENTIRE THINKING PROCESS
    institution_location_hierarchy = models.JSONField(null=True)
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
    institution_status = models.CharField(max_length=100, choices=STATUS, default="1")
    TYPE = [(1, "Formal"), (2, "Informal")]
    institution_type = models.CharField(
        max_length=100, choices=TYPE, default="1", null=False
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



class CustomUser(AbstractUser):
    user_type_data = (
        (1, "Admin"),
        (2, "Staff"),
        (3, "Student"),
        (4, "HOD"),
        (5, "Guardian"),
        (6, "Teacher"),
        (7, "Specialuser"),
    )
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    objects = models.Manager()


class HOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING)
    CONTRACT_TYPE = [
        (1, "Permanent"),
        (2, "Long Term"),
        (3, "Short Term"),
        (4, "Contracted Labour"),
        (5, "Probation"),
    ]
    contract_type = models.CharField(default=5, choices=CONTRACT_TYPE, max_length=50)
    phonenumber = models.CharField(max_length=12)
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.admin.first_name}  {self.admin.last_name}"


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=12, null=True)
    secondary_phone_number = models.CharField(max_length=12, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    ## implement the student registration number field properly
    pin_tax_number = models.CharField(max_length=12, null=True)
    nhif = models.CharField(max_length=12, null=True)
    social_security_number = models.CharField(max_length=12, null=True)
    industrial_training_number = models.CharField(max_length=12, null=True)
    statutory_numbers = models.JSONField(null=True)

    ## implement the student registration number field properly
    # o Bank 1
    # o Bank 2
    # o Bank 3
    # o Bank 4
    # o Mobile Money
    #  Pay Bill Number
    #  TILL Number

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

    # def __str__(self):
    #     return self.admin


class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    STAFF_TYPE = [(1, "Administration"), (2, "Support")]
    staff_type = models.CharField(default=1, choices=STAFF_TYPE, max_length=50)
    CONTRACT_TYPE = [
        (1, "Permanent"),
        (2, "Long Term"),
        (3, "Short Term"),
        (4, "Contracted Labour"),
        (5, "Probation"),
    ]
    contract_type = models.CharField(default=5, choices=CONTRACT_TYPE, max_length=50)
    description = models.CharField(max_length=255, null=True)
    contract_years = models.CharField(max_length=255, default="Parmanent")
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.admin.first_name}  {self.admin.last_name}"


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    institution_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255, default="institution", null=True)
    head = models.ForeignKey(HOD, on_delete=models.DO_NOTHING, null=True)
    deputy = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, null=True)


class Guardian(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING)
    phonenumber = models.CharField(max_length=12)
    bank = models.CharField(null=True, max_length=1000)
    gender = models.CharField(max_length=50)

    def __str__(self):
        return self.user.name


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # admission_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.JSONField(null=True)
    registration_number = models.CharField(max_length=10, unique=True, null=True)
    index_number = models.CharField(max_length=20, unique=True, null=True)
    profile_pic = models.FileField(null=True)
    address = models.TextField(null=True)
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    session_year_id = models.ForeignKey(
        Session, on_delete=models.DO_NOTHING, null=True
    )
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING, null=True)
    require_entry_exams = models.BooleanField(default=True)
    ENTRY_EXAM_TYPE = [(1, "Normal"), (2, "Special")]
    type_of_entry_exam = models.CharField(
        max_length=10, choices=ENTRY_EXAM_TYPE, default="1"
    )
    REGISTRATION_TYPE = [(1, "New"), (2, "Continuing")]
    registration_type = models.CharField(
        max_length=10, choices=REGISTRATION_TYPE, default="1"
    )
    STUDENT_TYPE = [(1, "Local"), (2, "International")]
    student_type = models.CharField(max_length=10, choices=STUDENT_TYPE, default="1")
    GENDER = [("1", "Male"), ("2", "Female")]
    gender = models.CharField(max_length=10, choices=GENDER, default="1")
    ACCOUNT_STATUS = [
        (1, "Active"),
        (2, "Inactive"),
        (3, "On-Hold"),
        (4, "Suspended"),
        (5, "Terminated"),
    ]
    account_status = models.CharField(
        max_length=10, choices=ACCOUNT_STATUS, default="1"
    )
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
    STUDENT_STUDY_TYPE = [(1, "Full Time"), (2, "Part Time"), (3, "Online")]
    study_type = models.CharField(
        max_length=10, choices=STUDENT_STUDY_TYPE, default="1"
    )
    STUDENT_BOARDING_TYPE = [(1, "Boarder"), (2, "Day-Scholer")]
    boarding_type = models.CharField(
        max_length=10, choices=STUDENT_BOARDING_TYPE, default="1"
    )
    STUDENT_SPONSORSHIP_TYPE = [(1, "Self-Sponsored"), (2, "Sponsored")]
    sponsorship_type = models.CharField(
        max_length=10, choices=STUDENT_SPONSORSHIP_TYPE, default="1"
    )
    STUDENT_SPONSOR_TYPE = [(1, "Government"), (2, "Organizations"), (3, "Sponsor")]
    sponsor_type = models.CharField(
        max_length=10, choices=STUDENT_SPONSOR_TYPE, default="1"
    )
    STUDENT_SPECIAL_NEEDS_TYPE = [
        (1, "Physically Impaired"),
        (2, "Visually Impaired"),
        (3, "Hearing Impaired"),
        (4, "Intellectually Impaired"),
        (5, "Multiple Disabilities"),
        (6, "Other Impairment"),
    ]
    special_needs = models.CharField(
        max_length=100, choices=STUDENT_SPECIAL_NEEDS_TYPE, default="1"
    )
    relationships = models.JSONField(null=True)
    religion = models.CharField(max_length=20, null=True)
    require_transport = models.BooleanField(default=False)

    # sample data
    # a. Blood Group
    # b. Height
    # c. Allergies
    # d. Special Conditions
    # e. Special Needs Leaner (Type of Special Needs)
    # f. Other Medical Details
    # g. Emergency Contact
    # - Name
    # - Relationship
    # - Postal Address
    # - Physical Address (Current Residence/Work)
    # - Telephone
    # - Email
    bio_data = models.JSONField(null=True)

    # . Pupil/Student Contacts
    # - Telephone
    # - Email Address
    # - Postal Address
    # - Physical Address
    student_contact = models.JSONField(null=True)

    # - Name
    # - Relationship
    # - Telephone
    # - Email Address
    # - Country
    # - Postal Address
    # - Physical Address
    # - Passport Size Photo
    sponsor_contact = models.JSONField(null=True)
    fee_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


#: TODO
## implement the student registration number field properly
# class Student(models.Model):
#     registration_number = models.CharField(max_length=10, unique=True, editable=False, default=generate_registration_number)
#     # other fields ...


def generate_registration_number():
    # code to generate unique registration number
    return "SCHOOL-" + str(uuid.uuid4().int)[:10]


class SpecialUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=12)

    def __str__(self):
        return self.user.name


# Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model


@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    def generate_registration_number(school):
        # code to generate unique registration number
        return f"SCHOOL-" + school[:5] + str(uuid.uuid4().int)[:10]

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
