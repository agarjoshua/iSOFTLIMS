# import os
import django
from faker import Faker

# from django.db import transaction
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iSOFTLIMS.settings')

django.setup()

from core.models import HOD, Admin, AdminType, Applicant, Department, Guardian, HODType, Institution, Staff, StaffType, Students, Teacher
from django.contrib.auth import get_user_model

fake = Faker()
User = get_user_model()

def generate_institutions(num):
    # Generate Institutions
    for _ in range(num):
        institution = Institution()
        institution.name = fake.company()
        institution.country = fake.country()
        institution.save()
        print('I created all the institutions, I guess?')

# def generate_institutions(num)

def generate_users(num):
    # Generate Users
    for _ in range(num):
        user = User()
        user.username = fake.user_name() # type: ignore
        user.email = fake.email() # type: ignore
        user.set_password(fake.password())
        user.save()
        

    # Generate Admins
    admins = User.objects.filter(user_type=User.ADMIN)  # type: ignore # Assuming ADMIN is the user_type for admins
    admin_types = AdminType.objects.all()
    
    for admin in admins:
        admin_profile = Admin()
        admin_profile.user = admin
        admin_profile.admin_type = fake.random_element(admin_types)
        admin_profile.save()

    # Generate HODs
    hods = User.objects.filter(user_type=User.HOD)  # type: ignore # Assuming HOD is the user_type for Head of Departments
    hod_types = HODType.objects.all()
    for hod in hods:
        hod_profile = HOD()
        hod_profile.user = hod
        hod_profile.hod_type = fake.random_element(hod_types)
        hod_profile.save()

    # Generate Teachers
    teachers = User.objects.filter(user_type=User.TEACHER)  # type: ignore # Assuming TEACHER is the user_type for teachers
    institutions = Institution.objects.all()
    for teacher in teachers:
        teacher_profile = Teacher()
        teacher_profile.user = teacher
        teacher_profile.name = fake.name()
        teacher_profile.phonenumber = fake.phone_number()
        teacher_profile.institution = fake.random_element(institutions)
        teacher_profile.save()

    # Generate Staff
    staff = User.objects.filter(user_type=User.STAFF)  # type: ignore # Assuming STAFF is the user_type for staff members
    staff_types = StaffType.objects.all()
    for staff_member in staff:
        staff_profile = Staff()
        staff_profile.user = staff_member
        staff_profile.associated_department = fake.random_element(departments)
        staff_profile.address = fake.address()
        staff_profile.telephone = fake.phone_number()
        staff_profile.email = fake.email()
        staff_profile.staff_type = fake.random_element(staff_types)
        staff_profile.save()

    # Generate Departments
    institutions = Institution.objects.all()
    for institution in institutions:
        for _ in range(3):  # Generate 3 departments per institution
            department = Department()
            department.name = fake.catch_phrase()
            department.description = fake.text()
            department.head = fake.random_element(User.objects.filter(user_type=User.HOD)) # type: ignore
            department.deputy = fake.random_element(User.objects.filter(user_type=User.TEACHER)) # type: ignore
            department.institution = institution
            department.save()

    # Generate Guardians
    guardians = User.objects.filter(user_type=User.GUARDIAN)  # Assuming GUARDIAN is the user_type for guardians
    for guardian in guardians:
        guardian_profile = Guardian()
        guardian_profile.user = guardian
        guardian_profile.phonenumber = fake.phone_number()
        guardian_profile.bank = fake.company()
        guardian_profile.gender = fake.random_element(['Male', 'Female'])
        guardian_profile.save()

    # Generate Students
    students = User.objects.filter(user_type=User.STUDENT)  # Assuming STUDENT is the user_type for students
    for student in students:
        student_profile = Students()
        student_profile.user = student
        student_profile.admission_number = fake.random_int(min=1000, max=9999)
        student_profile.name = fake.name()
        student_profile.registration_number = fake.random_int(min=100000, max=999999)
        student_profile.index_number = fake.random_int(min=10000, max=99999)
        student_profile.gender = fake.random_element(['Male', 'Female'])
        student_profile.save()

    # Generate Applicants
    applicants = User.objects.filter(user_type=User.APPLICANT)  # type: ignore # Assuming APPLICANT is the user_type for applicants
    for applicant in applicants:
        applicant_profile = Applicant()
        applicant_profile.user = applicant
        applicant_profile.surname = fake.last_name()
        applicant_profile.other_names = fake.first_name()
        applicant_profile.gender = fake.random_element(['Male', 'Female'])
        applicant_profile.nationality = fake.country()
        applicant_profile.id_or_passport_number = fake.random_int(min=10000, max=99999)
        applicant_profile.date_of_birth = fake.date_of_birth(minimum_age=16, maximum_age=30)
        applicant_profile.save()
    
    print('I created all the users, I guess IDK?')


def generate_mock_data(nums):
    # Generate HOD Types
    for _ in range(nums):
        hod_types = HODType.objects.all()
        for hod_type in hod_types:
            hod_type = HODType()
            hod_type.name = fake.name
            hod_type.save()

        # Generate Departments
        departments = Department.objects.all()
        for department in departments: 
            hod = HOD()
            hod.admin = fake.random_element(User.objects.filter(user_type=User.ADMIN))
            hod.hod_type = fake.random_element(HODType.objects.all())
            hod.associated_department = department
            hod.contract_type = fake.random_element([choice[0] for choice in HOD.CONTRACT_TYPE])
            hod.phonenumber = fake.phone_number()
            hod.save()


def generate 


# generate_users(2500)
generate_mock_data(5)