import ast
import random
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.core import exceptions
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from core import models
from core.forms.courseforms import AddCourseForm
from core.forms.departmentforms import AddDepartmentForm
from core.forms.guardianforms import AddGuardianForm, EditGuardianForm
from core.forms.hodforms import AddHodForm, AddStaffTypeForm, EditHodForm
from core.forms.institutionform import InstitutionForm
from core.forms.studentforms import EditStudentForm, AddStudentForm
from django.contrib.admin.views.decorators import user_passes_test # type: ignore

from core.models import (
    HOD,
    Applicant,
    ApplicantApprovalWorklow,
    CustomUser,
    Admin,
    Department,
    Guardian,
    Staff,
    StaffType,
    Students,
    Teacher,
    Institution,
    # Subjects,
    # FeedBackStudent,
    # FeedBackStaffs,
    # LeaveReportStudent,
    # LeaveReportStaff,S
    # Attendance,
    # AttendanceReport,
)
from academics.models import (
    Class,
    Course,
    Session,
)
from core.subviews.utilities.accesscontrolutilities import allow_user
# from core.forms import AddStudentForm, EditStudentForm

# USER NUMBER REFERENCE
# 1 = ADMIN
# 2 = STAFF
# 3 = STUDENTS
# 4 = HOD
# 5 = GUARDIAN
# 6 = TEACHER
 


@allow_user('1','2','3','4','5','6') 
def admin_home(request):
    all_teachers_count = Teacher.objects.all().count()
    all_student_count = Students.objects.all().count()
    # subject_count = Subjects.objects.all().count()
    staff_count = Staff.objects.all().count()

    # Total Subjects and students in Each Course
    # class_all = Class.objects.all()
    # class_name_list = []
    # subject_count_list = []
    # student_count_list_in_class = []

    # for class in class_all:
    #     subjects = Subjects.objects.filter(class_id=class.id).count()
    #     students = Students.objects.filter(class_id=class.id).count()
    #     class_name_list.append(class.class_name)
    #     subject_count_list.append(subjects)
    #     student_count_list_in_class.append(students)

    # subject_all = Subjects.objects.all()
    # subject_list = []
    # student_count_list_in_subject = []
    # for subject in subject_all:
    #     class = Class.objects.get(id=subject.class_id.id)
    #     student_count = Students.objects.filter(class_id=class.id).count()
    #     subject_list.append(subject.subject_name)
    #     student_count_list_in_subject.append(student_count)

    # For Saff
    staff_attendance_present_list = []
    staff_attendance_leave_list = []
    staff_name_list = []

    staffs = Staff.objects.all()
    # for staff in staffs:
    #     subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
    #     attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
    #     leaves = LeaveReportStaff.objects.filter(
    #         staff_id=staff.id, leave_status=1
    #     ).count()
    #     staff_attendance_present_list.append(attendance)
    #     staff_attendance_leave_list.append(leaves)
    #     staff_name_list.append(staff.admin.first_name)

    # For Students
    student_attendance_present_list = []
    student_attendance_leave_list = []
    student_name_list = []

    students = Students.objects.all()
    # for student in students:
    #     attendance = AttendanceReport.objects.filter(
    #         student_id=student.id, status=True
    #     ).count()
    #     absent = AttendanceReport.objects.filter(
    #         student_id=student.id, status=False
    #     ).count()
    #     leaves = LeaveReportStudent.objects.filter(
    #         student_id=student.id, leave_status=1
    #     ).count()
    #     student_attendance_present_list.append(attendance)
    #     student_attendance_leave_list.append(leaves + absent)
    #     student_name_list.append(student.admin.first_name)

    # For Teachers
    teachers = Students.objects.all()

    context = {
        "all_student_count": all_student_count,
        "staff_attendance_present_list": staff_attendance_present_list,
        "staff_attendance_leave_list": staff_attendance_leave_list,
        "staff_name_list": staff_name_list,
        "student_attendance_present_list": student_attendance_present_list,
        "student_attendance_leave_list": student_attendance_leave_list,
        "student_name_list": student_name_list,
        # "subject_count": subject_count,
        "staff_count": staff_count,
        # "class_name_list": class_name_list,
        # "subject_count_list": subject_count_list,
        # "student_count_list_in_class": student_count_list_in_class,
        # "subject_list": subject_list,
        # "student_count_list_in_subject": student_count_list_in_subject,
    }
    return render(request, "admin_template/home_content.html", context)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {"user": user}
    return render(request, "admin_template/admin_profile.html", context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("admin_profile")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect("admin_profile")
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect("admin_profile")


def school_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    school_id = Admin.objects.get(admin=request.user.id).institution
    form = InstitutionForm()

    context = {"user": user, "form": form}
    return render(request, "admin_template/school_profile.html", context)


def admin_school_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("school_profile")
    else:
        form = InstitutionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            country = form.cleaned_data["country"]
            institution_order = form.cleaned_data["institution_order"]
            #:TODO: build the tool needed for this data processing
            institution_location_hierarchy = form.cleaned_data[
                "institution_location_hierarchy"
            ]
            institution_cluster = form.cleaned_data["institution_cluster"]
            institution_category = form.cleaned_data["institution_category"]
            institution_gender_category = form.cleaned_data[
                "institution_gender_category"
            ]
            institution_accomodation_type = form.cleaned_data[
                "institution_accomodation_type"
            ]
            institution_status = form.cleaned_data["institution_status"]
            institution_type = form.cleaned_data["institution_type"]
            institution_in_ASAL_area = form.cleaned_data["institution_in_ASAL_area"]
            institution_residence = form.cleaned_data["institution_residence"]
            contact_details = form.contact_details()
            institution_statutory_numbers = form.other_statutory_details()
            currency = form.cleaned_data["currency"]
            bank_details = form.financial_details()

            try:
                specific_institution = Admin.objects.get(admin=request.user).institution
                specific_institution.specific_institution_id = Admin.objects.get(
                    admin=request.user
                ).institution
                specific_institution.name = name
                specific_institution.country = country
                specific_institution.institution_order = institution_order
                specific_institution.institution_location_hierarchy = (
                    institution_location_hierarchy
                )
                specific_institution.institution_cluster = institution_cluster
                specific_institution.institution_category = institution_category
                specific_institution.institution_gender_category = (
                    institution_gender_category
                )
                specific_institution.institution_in_ASAL_area = institution_in_ASAL_area
                specific_institution.institution_residence = institution_residence
                specific_institution.contact_details = contact_details
                specific_institution.institution_statutory_numbers = (
                    institution_statutory_numbers
                )
                specific_institution.currency = currency
                specific_institution.bank_details = bank_details
                specific_institution.save()
            except Exception as e:
                print(e)
                return e
        else:
            school_id = Admin.objects.get(admin=request.user.id).institution.id
            school = Institution.objects.get(id=school_id)
            form = InstitutionForm(initial=school)

    messages.success(request, "Profile Updated Successfully")
    return redirect("school_profile")
    # except Exception as e:
    #     # messages.error(request, "Failed to Update Profile")
    #     print(e)
    #     return redirect("school_profile")


def add_staff(request):
    staff_type = StaffType.objects.all()
    departments = Department.objects.all()
    print(departments)
    context = {
        "staff_type":staff_type,
        "departments":departments
    }
    return render(request, "admin_template/add_staff_template.html", context)


def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect("add_staff")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        staff_type = request.POST.get("staff_type")
        department = request.POST.get("department")

        staff_type = StaffType.objects.get(id=staff_type)

        

        name = f'{first_name} {last_name}'

        department = Department.objects.get(id=department)

        is_check = request.POST.get("check", False)

        user_type = 6 if is_check else 2

        try:
            user = CustomUser.objects.create_user(
                
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
                
            )
            # institution = Admin.objects.get(admin=request.user).institution
            if user_type == 2:
                user.staff.name=name
                user.staff.address = address
                user.staff.staff_type = staff_type
                user.staff.associated_department = department
            # elif user_type == 6:
            #     user.teacher.institution = institution
            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect("manage_staff")
        except Exception as e:
            # messages.error(request, "Failed to Add Staff!")
            print(e)
            messages.error(request, f"Failed to Add Staff - {e}!")
            return redirect("add_staff")


def manage_staff(request):
    staff = Staff.objects.all()
    teachers = Students.objects.all()
    
    
    context = {
        "staffs": staff, 
        "teachers": teachers,
        # "departments": departments
        }
    return render(request, "admin_template/manage_staff_template.html", context)


def edit_staff(request, staff_id):
    staff = Staff.objects.get(admin=staff_id)
    departments = Department.objects.all()
    context = {"staff": staff, "id": staff_id, "departments": departments}
    return render(request, "admin_template/edit_staff_template.html", context)


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get("staff_id")
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        department = request.POST.get("department")

        department = Department.objects.get(id=department)

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # INSERTING into Staff Model
            staff_model = Staff.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.associated_department = department
            staff_model.save()

            messages.success(request, "Staff Updated Successfully.")
            return redirect("/edit_staff/" + staff_id)

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect("/edit_staff/" + staff_id)


def delete_staff(request, staff_id):
    staff = Staff.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect("manage_staff")
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect("manage_staff")



def manage_staff_type(request):
    staff_types = StaffType.objects.all()
    staff_type_form = AddStaffTypeForm()
    context = {
        "staff_types": staff_types,
        "staff_type_form": staff_type_form
        }
    return render(request, "admin_template/manage_stafftype_template.html", context)

def create_staff_type(request):

    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("manage_staff_type")
    else:
        form = AddStaffTypeForm(request.POST)
        if form.is_valid():
            try:
                form.save() # type: ignore
                messages.success(request, 'Staff Type added succesfully')
                redirect('manage_staff_type')
            except Exception as e:
                messages.error(request, f'Staff not added. Error - {e}')
                redirect('manage_staff_type')
        else: 
            messages.error(request, 'Form is Invalid')
            redirect('manage_staff_type')
    return redirect('manage_staff_type')






#########################################MANAGE STUDENTS#######################################################################


def add_student(request):
    form = AddStudentForm()
    courses = Course.objects.all()
    context = {
        "form": form,
        "courses": courses,
        }
    return render(request, "admin_template/add_student_template.html", context)


def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("add_student")
    else:
        form = AddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            gender = form.cleaned_data["gender"]
            course = form.cleaned_data["course"]
            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES["profile_pic"]
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None
            student_type = form.cleaned_data["student_type"]
            account_status=form.cleaned_data["account_status"]
            academic_status =form.cleaned_data["academic_status"]
            study_type =form.cleaned_data["study_type"]
            boarding_type =form.cleaned_data["boarding_type"]
            sponsorship_type =form.cleaned_data["sponsorship_type"]
            sponsor_type =form.cleaned_data["sponsor_type"]
            special_needs =form.cleaned_data["special_needs"]
            require_transport =form.cleaned_data["require_transport"]


            try:
                user = CustomUser.objects.create_user(
                    username=first_name,
                    password=first_name,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    user_type=3,
                )
                
                user.students.name = f'{first_name} {last_name}'
                user.students.registration_number = f'{study_type}/{first_name}/{last_name}'
                user.students.index_number = lambda: ''.join(random.choices('0123456789', k=7))
                user.students.profile_pic_url = profile_pic_url
                user.students.address = address
                course = Course.objects.get(id=course.id)
                user.students.course = course
                user.students.student_type = student_type
                user.students.gender = gender
                user.students.account_status = account_status
                user.students.academic_status = academic_status
                user.students.study_type = study_type
                user.students.boarding_type = boarding_type
                user.students.sponsorship_type = sponsorship_type
                user.students.sponsor_type = sponsor_type
                user.students.special_needs = special_needs
                user.students.require_transport = require_transport

                user.save()
                messages.success(request, "Student Added Successfully!")
                return redirect("manage_students")

            except Exception as e:
                messages.error(request, f"Failed to Add Student! -{e}")
                print(e)
                return redirect("manage_students")
        else:
            error_list = []
            for field, errors in form.errors.items():
                error_list.append(f"{field}: {', '.join(errors)}")
            print(error_list)
            messages.error(request, f"Form is not valid because {error_list}")
            return redirect("add_student")


def manage_students(request):
    students = Students.objects.all()
    context = {"students": students}
    return render(request, "admin_template/manage_student_template.html", context)


def edit_student(request, student_id):
    # Adding Student ID into Session Variable
    request.session["student_id"] = student_id

    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    # Filling the form with Data from Database
    form.fields["email"].initial = student.admin.email
    form.fields["username"].initial = student.admin.username
    form.fields["first_name"].initial = student.admin.first_name
    form.fields["last_name"].initial = student.admin.last_name
    form.fields["address"].initial = student.address
    form.fields["class_id"].initial = student.class_id.id
    form.fields["gender"].initial = student.gender
    form.fields["session_year_id"].initial = student.session_year_id.id

    context = {"id": student_id, "username": student.admin.username, "form": form}
    return render(request, "admin_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            print('-------------------------------------------')
            print(form)
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            address = form.cleaned_data["address"]
            class_id = form.cleaned_data["class_id"]
            gender = form.cleaned_data["gender"]
            session_year_id = form.cleaned_data["session_year_id"]

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES["profile_pic"]
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Students Table
                student_model = Students.objects.get(admin=student_id)
                student_model.address = address

                session_year_obj = Session.objects.get(id=session_year_id)
                student_model.session_year_id = session_year_obj

                student_model.gender = gender
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session["student_id"]

                messages.success(request, "Student Updated Successfully!")
                return redirect("/edit_student/" + student_id)
            except:
                messages.success(request, "Failed to Uupdate Student.")
                return redirect("/edit_student/" + student_id)
        else:
            return redirect("/edit_student/" + student_id)


def delete_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect("manage_students")
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect("manage_students")


#########################################MANAGE PARENTS#######################################################################

def manage_guardians(request):
    guardians = Guardian.objects.all()
    context = {"guardians": guardians}
    return render(request, "admin_template/manage_guardian_template.html", context)


def add_guardian(request):
    form = AddGuardianForm()
    context = {"form": form}
    return render(request, "admin_template/add_guardian_template.html", context)


def add_guardian_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("add_guardian")
    else:
        form = AddGuardianForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            phonenumber = form.cleaned_data["phonenumber"]
            bank = form.cleaned_data["bank"]
            gender = form.cleaned_data["gender"]

            try:
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    user_type=5,
                )

                # institution = Admin.objects.get(admin=request.user).institution
                # user.guardian.institution = institution
                user.guardian.phonenumber = phonenumber
                user.guardian.bank = bank
                user.guardian.gender = gender
                user.save()
                messages.success(request, "Guardian Added Successfully!")
                return redirect("add_guardian")
            except Exception as e:
                messages.error(request, "Failed to Add Guardian!")
                print(e)
                return redirect("add_guardian")
        else:
            return redirect("add_guardian")


def edit_guardian(request, guardian_id):
    # Adding Guardian ID into Session Variable
    request.session["guardian_id"] = guardian_id

    guardian = Guardian.objects.get(admin=guardian_id)
    form = EditGuardianForm()
    # Filling the form with Data from Database
    form.fields["email"].initial = guardian.admin.email
    form.fields["username"].initial = guardian.admin.username
    form.fields["first_name"].initial = guardian.admin.first_name
    form.fields["last_name"].initial = guardian.admin.last_name
    form.fields["bank"].initial = guardian.bank
    form.fields["phonenumber"].initial = guardian.phonenumber
    form.fields["gender"].initial = guardian.gender

    context = {"id": guardian_id, "username": guardian.admin.username, "form": form}
    return render(request, "admin_template/edit_guardian_template.html", context)


def edit_guardian_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        guardian_id = request.session.get("guardian_id")
        if guardian_id == None:
            return redirect("/guardian_id")

        form = EditGuardianForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            phonenumber = form.cleaned_data["phonenumber"]
            bank = form.cleaned_data["bank"]
            gender = form.cleaned_data["gender"]

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=guardian_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Guardians Table
                guardian_model = Guardian.objects.get(admin=guardian_id)
                guardian_model.phonenumber = phonenumber
                guardian_model.bank = bank
                guardian_model.gender = gender
                guardian_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session["guardian_id"]

                messages.success(request, "Student Updated Successfully!")
                return redirect("/edit_guardian/" + guardian_id)
            except:
                messages.success(request, "Failed to Uupdate Student.")
                return redirect("/edit_guardian/" + guardian_id)
        else:
            return redirect("/edit_guardian/" + guardian_id)


def delete_student(request, guardian_id):
    guardian = Guardian.objects.get(admin=guardian_id)
    try:
        guardian.delete()
        messages.success(request, "Guardian Deleted Successfully.")
        return redirect("manage_guardians")
    except:
        messages.error(request, "Failed to Delete Guardian.")
        return redirect("manage_guardians")


#########################################MANAGE HOD#######################################################################

def manage_hods(request):
    hod = HOD.objects.all()
    context = {"hod": hod}
    return render(request, "admin_template/manage_hod_template.html", context)


def add_hod(request):
    form = AddHodForm()
    context = {"form": form}
    return render(request, "admin_template/add_hod_template.html", context)


def add_hod_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("add_hod")
    else:
        form = AddHodForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            phonenumber = form.cleaned_data["phonenumber"]
            hod_type = form.cleaned_data["hod_type"]
            associated_department = form.cleaned_data["associated_department"]

            associated_department = Department.objects.get(id=associated_department.id)

            try:
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    user_type=4,
                )

                # institution = Admin.objects.get(admin=request.user).institution
                # user.guardian.institution = institution
                user.hod.phonenumber = phonenumber
                user.hod.hod_type = hod_type
                user.hod.associated_department = associated_department
                user.save()
                messages.success(request, "HOD Added Successfully!")
                return redirect("manage_hod")
            except Exception as e:
                messages.error(request, "Failed to Add HOD!")
                print(e)
                return redirect("manage_hod")
        else:
            return redirect("manage_hod")


def edit_hod(request, hod_id):
    # Adding Guardian ID into Session Variable
    request.session["hod_id"] = hod_id

    hod = HOD.objects.get(admin=hod_id)
    form = EditHodForm()
    # Filling the form with Data from Database
    form.fields["email"].initial = hod.admin.email
    form.fields["username"].initial = hod.admin.username
    form.fields["first_name"].initial = hod.admin.first_name
    form.fields["last_name"].initial = hod.admin.last_name
    form.fields["phonenumber"].initial = hod.phonenumber
    form.fields["hod_type"].initial = hod.hod_type
    form.fields["associated_department"].initial =  hod.associated_department

    context = {"id": hod_id, "username": hod.admin.username, "form": form}
    return render(request, "admin_template/edit_hod_template.html", context)


def edit_hod_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        hod_id = request.session.get("hod_id")
        if hod_id == None:
            return redirect("/hod_id")

        form = EditHodForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            phonenumber = form.cleaned_data["phonenumber"]
            hod_type = form.cleaned_data["hod_type"]
            associated_department = form.cleaned_data["associated_department"]

            associated_department = Department.objects.get(id=associated_department.id)

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=hod_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Hod Table
                hod_model = HOD.objects.get(admin=hod_id)
                hod_model.phonenumber = phonenumber
                hod_model.hod_type = hod_type 
                hod_model.associated_department = associated_department
                hod_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session["hod_id"]

                messages.success(request, "Head of Departnment Updated Successfully!")
                return redirect("/edit_hod/" + hod_id)
            except Exception as e:
                messages.error(request, f"Failed to Update Hod. - {e}")
                return redirect("/edit_hod/" + hod_id)
        else:
            return redirect("/edit_hod/" + hod_id)


def delete_hod(request, hod_id):
    hod = HOD.objects.get(admin=hod_id)
    try:
        hod.delete()
        messages.success(request, "HOD Deleted Successfully.")
        return redirect("manage_hod")
    except:
        messages.error(request, "Failed to Delete HOD.")
        return redirect("manage_hod")



#########################################MANAGE ADMISSIONS#######################################################################
def admissions(request):
    approved_applicants = Applicant.objects.filter(applicantapprovalworklow__finance_approved=True)
    applicant_approval_workflow_admissions = Applicant.objects.filter(applicantapprovalworklow__department_approved=True)
    applicant_approval_workflow_dvc = Applicant.objects.filter(applicantapprovalworklow__dvc_approved=True)

    dvc_level = False

    try:
        dvc_level = Admin.objects.get(admin=request.user.id)
        if dvc_level:
            dvc_level = True
    
    except Exception as e:
        show_hod_div = False
    
    try:
        specified_hod = HOD.objects.get(admin=request.user.id)
        hod_dept = specified_hod.associated_department # type: ignore
        show_hod_div = hod_dept.name == 'Admissions'
    except Exception as e:
        show_hod_div = False
        
    context = {
        "approved_applicants":approved_applicants,
        "applicant_approval_workflow":applicant_approval_workflow_admissions,
        "applicant_approval_workflow_dvc":applicant_approval_workflow_dvc,
        "hod_level":show_hod_div,
        "dvc_level": dvc_level
    }
    return render(request, "admin_template/manage_admissions_template.html", context)


def admissions_approve(request):
    applicant_id = request.POST.get("selected_id")
    applicant = Applicant.objects.get(applicant_id=applicant_id)
    selected_applicant = ApplicantApprovalWorklow.objects.get(applicant=applicant)

    try:
        selected_applicant = ApplicantApprovalWorklow.objects.get(applicant=applicant)
        selected_applicant.department_approved = True
        selected_applicant.save()
        return redirect('admissions')
    except Exception as e:
        return HttpResponse(e)



def dvc_approve(request):
    applicant_id = request.POST.get("selected_id")
    applicant = Applicant.objects.get(applicant_id=applicant_id)
    selected_applicant = ApplicantApprovalWorklow.objects.get(applicant=applicant)

    try:
        selected_applicant = ApplicantApprovalWorklow.objects.get(applicant=applicant)
        selected_applicant.dvc_approved = True
        selected_applicant.save()

        applicant = Applicant.objects.get(applicant_id=applicant_id)
        return redirect('admissions')
    except Exception as e:
        return HttpResponse(e)



def manage_departments(request):
    department = Department.objects.all()
    context = {"department": department}
    return render(request, "admin_template/manage_department_template.html", context)


def add_department(request):
    staff = Staff.objects.all()
    hod = HOD.objects.all()
    context = {"staff": staff, "hod": hod}
    return render(request, "admin_template/add_department_template.html", context)


def add_department_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect("manage_department")
    else:
        name = request.POST.get("name")
        description = request.POST.get("description")
        head = request.POST.get("head")
        deputy = request.POST.get("deputy")

        try:
            department = Department.objects.create(
                name=name,
                description=description,
            )
            department.save()
            messages.success(request, "Department Added Successfully!")
            return redirect("manage_departments")
        except Exception as e:
            messages.error(request, "Failed to Add Department!")
            print(e)
            return redirect("add_department")


def edit_department(request, department_id):
    department = Department.objects.get(id=department_id)
    staff = Staff.objects.all()
    hod = HOD.objects.all()
    context = {
        "department": department,
        "department_id": department_id,
        "staff": staff,
        "hod": hod,
    }
    return render(request, "admin_template/edit_department_template.html", context)


def edit_department_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        head = request.POST.get("head")
        deputy = request.POST.get("deputy")
        department_id = request.POST.get("department_id")
        print(department_id)

        try:
            department = Department.objects.get(id=department_id)
            if name:
                department.name = name
            if desc:
                department.desc = desc
            if head:
                dep_head = HOD.objects.get(admin=head)
                department.head = dep_head
            if deputy:
                dep_deputy = Staff.objects.get(admin=deputy)
                department.deputy = dep_deputy

            messages.success(request, "Department upated Successfully!")
            return redirect("manage_departments")
        except Exception as e:
            messages.error(request, "Failed to upate Department!")
            print(e)
            return redirect("manage_departments")


def delete_department(request, department_id):
    pass

#########################################MANAGE COURSES#######################################################################

def manage_courses(request):
    form = AddCourseForm()
    courses = Course.objects.all()
    context = {
        "form":form,
        "courses":courses
    }
    return render(request,'admin_template/manage_courses_template.html',context)


def add_course(request):
    form = AddCourseForm()
    context = {
        "form":form
    }

    return render(request,'admin_template/add_course_template.html', context)


def add_course_save(request):
    print('helloooo')
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("manage_courses")
    else:
        form = AddCourseForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Course Added Successfully!")
                return redirect("manage_courses")
            except Exception as e:
                messages.error(request, f"Failed to Add Course - {e}!")
                return redirect("add_course")
        messages.error(request, "Form is not valid!")
        return redirect("add_course")
        

# def check_if_course_exists(request):
#     pass

@csrf_exempt
def check_if_course_exists(request):
    name = request.POST.get("course_name")
    """
    Checks if a course with the given name already exists, regardless of the case of the input string.
    Returns True if a course with the same name exists, False otherwise.
    """
    test = Course.objects.filter(course_name__iexact=name).exists()
    if test:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def edit_course(request):
    pass

def delete_course(request):
    pass

#########################################MANAGE SESSIONS#######################################################################


def manage_session(request):
    session_years = Session.objects.all()
    context = {"session_years": session_years}
    return render(request, "admin_template/manage_session_template.html", context)


def add_session(request):
    return render(request, "admin_template/add_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("add_session")
    else:
        session_start_date = request.POST.get("session_start_date")
        session_end_date = request.POST.get("session_end_date")
        is_current = request.POST.get("is_current") == "on"

        if is_current:
            Session.objects.all().update(is_current=False)

        try:
            sessionyear = Session(
                session_start_date=session_start_date, 
                session_end_date=session_end_date,
                is_current = is_current
            )
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("manage_session")
        except exceptions.ValidationError as e:
            messages.error(
                request,
                f"Failed to Add Session Year Due to incomplete or incorrect entry of fields (i.e {e})",
            )
            return redirect("manage_session")
        except Exception as e:
            messages.error(request, f"Failed to Add Session Year (i.e {e})")
            return redirect("add_session")


def edit_session(request, session_id):
    session_year = Session.objects.get(id=session_id)
    context = {"session_year": session_year}
    return render(request, "admin_template/edit_session_template.html", context)


def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("manage_session")
    else:
        session_id = request.POST.get("session_id")
        session_start_year = request.POST.get("session_start_year")
        session_end_year = request.POST.get("session_end_year")
        is_current = request.POST.get("is_current") == "on"

        if is_current:
            Session.objects.all().update(is_current=False)

        try:
            session_year = Session.objects.get(id=session_id)
            session_year.session_start_date = session_start_year
            session_year.session_end_date = session_end_year
            session_year.is_current = is_current
            print(session_year)
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect("/edit_session/" + session_id)
        except Exception as e:
            messages.error(request, f"Failed to Update Session Year. -{e}")
            return redirect("/edit_session/" + session_id)


def delete_session(request, session_id):
    session = Session.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect("manage_session")
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect("manage_session")


#########################################UTILITIES#######################################################################
@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

