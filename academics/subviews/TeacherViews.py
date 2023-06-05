import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from core.models import CustomUser, Teacher
from academics.models import ClassAttendance, ClassEnrollment, Course, Class, Students, Session, ExamResult
# from dateutil.parser import parse
from django.contrib import messages

# Attendance, AttendanceReport, LeaveReportStaff, FeedBackTeacher,

def teacher_home(request):
    # Fetching All Students under Staff

    subjects = Class.objects.filter(teacher=request.user.id)
    course_id_list = []
    # for subject in subjects:
    #     course = Course.objects.get(id=subject.course_id.id)
    #     course_id_list.append(course.id)
    
    final_course = []
    # Removing Duplicate Course Id
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)
    
    # students_count = Students.objects.filter(course_id__in=final_course).count()
    subject_count = subjects.count()

    # Fetch All Attendance Count
    # attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
    # Fetch All Approve Leave

    # staff = Teacher.objects.get(admin=request.user.id)

    # leave_count = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()

    #Fetch Attendance Data by Subjects
    subject_list = []
    attendance_list = []
    for subject in subjects:
        # attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        # attendance_list.append(attendance_count1)

    # students_attendance = Students.objects.filter(course_id__in=final_course)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    # for student in students_attendance:
        # attendance_present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
        # attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
        # student_list.append(student.admin.first_name+" "+ student.admin.last_name)
        # student_list_attendance_present.append(attendance_present_count)
        # student_list_attendance_absent.append(attendance_absent_count)

    context = {
        
        # "students_count": students_count,
        # "attendance_count": attendance_count,
        # "leave_count": leave_count,
        "subject_count": subject_count,
        "subject_list": subject_list,
        "attendance_list": attendance_list,
        "student_list": student_list,
        "attendance_present_list": student_list_attendance_present,
        "attendance_absent_list": student_list_attendance_absent

    }
    return render(request, "teacher_templates/teacher_home_template.html", context)



def teacher_take_attendance(request):
    teacher_obj = Teacher.objects.get(admin=request.user.id)
    classes = Class.objects.filter(teacher=teacher_obj)
    session_years = Session.objects.filter(is_current=True) # type: ignore
    context = {
        "classes": classes,
        "session_years": session_years
    }
    return render(request, "teacher_template/teacher_attendance_template.html", context)


def staff_apply_leave(request):
    staff_obj = Teacher.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, "staff_template/staff_apply_leave_template.html", context)


def staff_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff_obj = Teacher.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('staff_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('staff_apply_leave')


def staff_feedback(request):
    staff_obj = Teacher.objects.get(admin=request.user.id)
    feedback_data = FeedBackTeacher.objects.filter(staff_id=staff_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "staff_template/staff_feedback_template.html", context)


def staff_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Teacher.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackTeacher(staff_id=staff_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('staff_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('staff_feedback')


# WE don't need csrf_token when using Ajax
# @csrf_exempt
def get_students(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    class_id = Class.objects.get(id=subject_id)
    class_enrollments = ClassEnrollment.objects.filter(selected_class_id=class_id)
    students = Students.objects.filter(classenrollment__in=class_enrollments)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in students:
        data_small = {
            "id": student.admin.id,
            "name": f"{student.admin.first_name} {student.admin.last_name}",
        }
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_attendance_data(request):
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    student_ids = request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")


    class_model = Class.objects.get(id=subject_id)
    # session_year_model = Session.objects.get(id=session_year_id)


    json_student = json.loads(student_ids)
    # print(dict_student[0]['id'])

    # print(student_ids)
    try:
        # First Attendance Data is Saved on Attendance Model
        attendance = ClassAttendance(classroom_id=class_model.id, datetime=parse(attendance_date))
        attendance.save()

        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except Exception as e:
        print(e)
        return HttpResponse(f"{e}")




def teacher_update_attendance(request):
    teacher_obj = Teacher.objects.get(admin=request.user.id)
    classes = Class.objects.filter(teacher=teacher_obj)
    session_years = Session.objects.all()
    context = {
        "classes": classes,
        "session_years": session_years
    }
    return render(request, "teacher_template/update_attendance_template.html", context)


@csrf_exempt
def get_attendance_dates(request):
    

    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    # session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Class
    # Getting all data from subject model based on subject_id
    class_model = Class.objects.get(id=subject_id)

    # session_model = Session.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = ClassAttendance.objects.filter(classroom_id=class_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.datetime)}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = ClassAttendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small = {
            "id": student.student_id.admin.id,
            "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,
            "status": student.status,
        }
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def update_attendance_data(request):
    student_ids = request.POST.get("student_ids")

    attendance_date = request.POST.get("attendance_date")
    attendance = ClassAttendance.objects.get(id=attendance_date)

    json_student = json.loads(student_ids)

    try:
        
        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(admin=stud['id'])

            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status=stud['status']

            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def teacher_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Teacher.objects.get(admin=user)

    context={
        "user": user,
        "staff": staff
    }
    return render(request, 'staff_template/staff_profile.html', context)


def staff_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('staff_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Teacher.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('staff_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('staff_profile')



def teacher_manage_results(request):

    teacher_obj = Teacher.objects.get(admin=request.user.id)
    classes = Class.objects.filter(teacher=teacher_obj)

    session_years = Session.objects.all()
    context = {
        "classes": classes,
        "session_years": session_years,
    }
    return render(request, "teacher_template/add_results_template.html", context)


def teacher_add_result_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_add_result')
    else:
        student_admin_id = request.POST.get('student_list')
        assignment_marks = request.POST.get('assignment_marks')
        exam_marks = request.POST.get('exam_marks')
        subject_id = request.POST.get('subject')

        student_obj = Students.objects.get(admin=student_admin_id)
        subject_obj = Subjects.objects.get(id=subject_id)

        try:
            # Check if Students Result Already Exists or not
            check_exist = ExamResult.objects.filter(subject_id=subject_obj, student_id=student_obj).exists()
            if check_exist:
                result = ExamResult.objects.get(subject_id=subject_obj, student_id=student_obj)
                result.subject_assignment_marks = assignment_marks
                result.subject_exam_marks = exam_marks
                result.save()
                messages.success(request, "Result Updated Successfully!")
                return redirect('staff_add_result')
            else:
                result = ExamResult(student_id=student_obj, subject_id=subject_obj, subject_exam_marks=exam_marks, subject_assignment_marks=assignment_marks)
                result.save()
                messages.success(request, "Result Added Successfully!")
                return redirect('staff_add_result')
        except:
            messages.error(request, "Failed to Add Result!")
            return redirect('staff_add_result')


# def teacher_home(request):
#     context = {

#     }

#     return render(request, "teacher_template/teacher_home_template.html", context)

# def teacher_profile(request):

#     context = {
        
#     }
#     return render(request, "teacher_template/teacher_home_template.html", context)

# def manage_attendance(request):

#     context = {
        
#     }
#     return render(request, "teacher_template/teacher_home_template.html", context)