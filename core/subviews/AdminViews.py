from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from core.forms.departmentforms import AddDepartmentForm
from core.forms.guardianforms import AddGuardianForm, EditGuardianForm
from core.forms.hodforms import AddHodForm, EditHodForm
from core.forms.studentforms import EditStudentForm, AddStudentForm

from core.models import (
    HOD,
    CustomUser,
    Admin,
    Department,
    Guardian,
    Staff,
    Students,
    Teacher,
    Institution,
    Courses,
    # Subjects,
    SessionYearModel,
    # FeedBackStudent,
    # FeedBackStaffs,
    # LeaveReportStudent,
    # LeaveReportStaff,
    # Attendance,
    # AttendanceReport,
)

# from core.forms import AddStudentForm, EditStudentForm


def admin_home(request):
    all_teachers_cvount = Teacher.objects.all().count()
    all_student_count = Students.objects.all().count()
    # subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()
    staff_count = Staff.objects.all().count()

    # Total Subjects and students in Each Course
    # course_all = Courses.objects.all()
    # course_name_list = []
    # subject_count_list = []
    # student_count_list_in_course = []

    # for course in course_all:
    #     subjects = Subjects.objects.filter(course_id=course.id).count()
    #     students = Students.objects.filter(course_id=course.id).count()
    #     course_name_list.append(course.course_name)
    #     subject_count_list.append(subjects)
    #     student_count_list_in_course.append(students)

    # subject_all = Subjects.objects.all()
    # subject_list = []
    # student_count_list_in_subject = []
    # for subject in subject_all:
    #     course = Courses.objects.get(id=subject.course_id.id)
    #     student_count = Students.objects.filter(course_id=course.id).count()
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
        "course_count": course_count,
        "staff_count": staff_count,
        # "course_name_list": course_name_list,
        # "subject_count_list": subject_count_list,
        # "student_count_list_in_course": student_count_list_in_course,
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
    school = Admin.objects.get(admin=request.user.id).institution

    context = {"school": school, "user": user}
    return render(request, "admin_template/school_profile.html", context)


def admin_school_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("school_profile")
    else:
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        # logo = request.POST.get('password')
        # print(name, desc)

        try:
            institution = Institution(
                name=name,
                desc=desc,
            )
            institution.save()
            print(institution.name)
            # institution.institution = institution
            # institution.name = name
            # institution.desc = desc
            admin = Admin.objects.get(admin=request.user)
            admin.institution = institution
            admin.save()
            print(admin)

            messages.success(request, "Profile Updated Successfully")
            return redirect("school_profile")
        except Exception as e:
            # messages.error(request, "Failed to Update Profile")
            print(e)
            return redirect("school_profile")


def add_staff(request):
    return render(request, "admin_template/add_staff_template.html")


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
            institution = Admin.objects.get(admin=request.user).institution
            if user_type == 2:
                user.staff.address = address
                user.staff.institution = institution
            elif user_type == 6:
                user.teacher.institution = institution
            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect("add_staff")
        except Exception as e:
            # messages.error(request, "Failed to Add Staff!")
            print(e)
            return redirect("add_staff")


def manage_staff(request):
    staff = Staff.objects.all()
    teachers = Students.objects.all()
    context = {"staffs": staff, "teachers": teachers}
    return render(request, "admin_template/manage_staff_template.html", context)


def edit_staff(request, staff_id):
    staff = Staff.objects.get(admin=staff_id)

    context = {"staff": staff, "id": staff_id}
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


#########################################MANAGE STUDENTS#######################################################################


def add_student(request):
    form = AddStudentForm()
    context = {"form": form}
    return render(request, "admin_template/add_student_template.html", context)


def add_student_save(request):
    print("-------------------------------------")
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("add_student")
    else:
        form = AddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course_id"]
            gender = form.cleaned_data["gender"]

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
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    user_type=3,
                )
                user.students.address = address

                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj

                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session_year_obj

                user.students.gender = gender
                user.students.profile_pic = profile_pic_url

                institution = Admin.objects.get(admin=request.user).institution
                user.students.institution = institution

                user.save()
                messages.success(request, "Student Added Successfully!")
                return redirect("add_student")
            except Exception as e:
                messages.error(request, "Failed to Add Student!")
                print(e)
                return redirect("add_student")
        else:
            return redirect("add_student")


def manage_student(request):
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
    form.fields["course_id"].initial = student.course_id.id
    form.fields["gender"].initial = student.gender
    form.fields["session_year_id"].initial = student.session_year_id.id

    context = {"id": student_id, "username": student.admin.username, "form": form}
    return render(request, "admin_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.session.get("student_id")
        if student_id == None:
            return redirect("/manage_student")

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            address = form.cleaned_data["address"]
            course_id = form.cleaned_data["course_id"]
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

                course = Courses.objects.get(id=course_id)
                student_model.course_id = course

                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
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
        return redirect("manage_student")
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect("manage_student")


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
                user.save()
                messages.success(request, "HOD Added Successfully!")
                return redirect("add_hod")
            except Exception as e:
                messages.error(request, "Failed to Add HOD!")
                print(e)
                return redirect("add_hod")
        else:
            return redirect("add_hod")


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
                hod_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session["hod_id"]

                messages.success(request, "Student Updated Successfully!")
                return redirect("/edit_hod/" + hod_id)
            except:
                messages.success(request, "Failed to Update Hod.")
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


#########################################MANAGE DEPARTMENTS#######################################################################


def manage_departments(request):
    department = Department.objects.all()
    context = {"department": department}
    return render(request, "admin_template/manage_department_template.html", context)


def add_department(request):
    staff = Staff.objects.all()
    hod = HOD.objects.all()
    context = {"staff":staff, "hod": hod}
    return render(request, "admin_template/add_department_template.html", context)


def add_department_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect("add_staff")
    else:
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        head = request.POST.get("head")
        deputy = request.POST.get("deputy")

        dep_head = HOD.objects.get(admin=head)
        dep_deputy = Staff.objects.get(admin=deputy)

        try:
            department = Department.objects.create(
                name=name,
                desc=desc,
                head=dep_head,
                deputy=dep_deputy,
            )
            department.save()
            messages.success(request, "Department Added Successfully!")
            return redirect("add_department")
        except Exception as e:
            messages.error(request, "Failed to Add Department!")
            print(e)
            return redirect("add_department")

def edit_department(request, department_id):
    department = Department.objects.get(id=department_id)
    staff = Staff.objects.all()
    hod = HOD.objects.all()
    context = {"department": department, "department_id": department_id, "staff":staff,"hod":hod}
    return render(request, "admin_template/edit_department_template.html", context)


def edit_department_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        head = request.POST.get("head")
        print(head)
        deputy = request.POST.get("deputy")

        dep_head = HOD.objects.get(admin=head)
        print("---------------------------------------------------")
        print(head)
        print("---------------------------------------------------")
        dep_deputy = Staff.objects.get(admin=deputy)

        department_id = request.POST.get("department_id")

        try:
            department = Department.objects.get(id=department_id)
            department.name=name,
            department.desc=desc,
            department.head=dep_head,
            department.deputy=dep_deputy,
            
            department.save()
            messages.success(request, "Department upated Successfully!")
            return redirect("edit_department")
        except Exception as e:
            messages.error(request, "Failed to upated Department!")
            print(e)
            return redirect("edit_department")


def delete_department(request, department_id):
    pass


#########################################MANAGE COURSES#######################################################################
def add_course(request):
    return render(request, "admin_template/add_course_template.html")


def add_course_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("add_course")
    else:
        course = request.POST.get("course")
        cost = request.POST.get("fee")
        try:
            course_model = Courses(course_name=course, cost=cost)
            course_model.save()
            messages.success(request, "Course Added Successfully!")
            return redirect("add_course")
        except:
            messages.error(request, "Failed to Add Course!")
            return redirect("add_course")


def manage_course(request):
    courses = Courses.objects.all()
    context = {"courses": courses}
    return render(request, "admin_template/manage_course_template.html", context)


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    context = {"course": course, "id": course_id}
    return render(request, "admin_template/edit_course_template.html", context)


def edit_course_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course")
        cost = request.POST.get("course")

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.cost = cost
            course.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect("/edit_course/" + course_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect("/edit_course/" + course_id)


def delete_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    try:
        course.delete()
        messages.success(request, "Course Deleted Successfully.")
        return redirect("manage_course")
    except:
        messages.error(request, "Failed to Delete Course.")
        return redirect("manage_course")


#########################################MANAGE SESSIONS#######################################################################


def manage_session(request):
    session_years = SessionYearModel.objects.all()
    context = {"session_years": session_years}
    return render(request, "admin_template/manage_session_template.html", context)


def add_session(request):
    return render(request, "admin_template/add_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("add_course")
    else:
        session_start_year = request.POST.get("session_start_year")
        session_end_year = request.POST.get("session_end_year")

        try:
            sessionyear = SessionYearModel(
                session_start_year=session_start_year, session_end_year=session_end_year
            )
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("add_session")
        except:
            messages.error(request, "Failed to Add Session Year")
            return redirect("add_session")


def edit_session(request, session_id):
    session_year = SessionYearModel.objects.get(id=session_id)
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

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect("/edit_session/" + session_id)
        except:
            messages.error(request, "Failed to Update Session Year.")
            return redirect("/edit_session/" + session_id)


def delete_session(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
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
