from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.utils import timezone
from academics.models import Class, ClassEnrollment, ClusterClass, Enrollment, Session
from core.forms.studentforms import DefferementApprovalWorkflowForm, TemporaryWithdrawalApprovalWorklowForm # To Parse input DateTime into Python Date Time Object

from core.models import Booking, DeferrmentApprovalWorklow, House, Students,CustomUser, TemporaryWithdrawalApprovalWorklow
from core.subviews.utilities.StudentViewUtilities import check_student_is_defferred, check_student_is_temporarily_withdrawn
# Staffs, Courses, Subjects,  Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult


def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    # total_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
    # attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    # attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status=False).count()

    # course_obj = Courses.objects.get(id=student_obj.course_id.id)
    # total_subjects = Subjects.objects.filter(course_id=course_obj).count()

    subject_name = []
    data_present = []
    data_absent = []
    # subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    # for subject in subject_data:
    #     attendance = Attendance.objects.filter(subject_id=subject.id)
    #     attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, student_id=student_obj.id).count()
    #     attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, student_id=student_obj.id).count()
    #     subject_name.append(subject.subject_name)
    #     data_present.append(attendance_present_count)
    #     data_absent.append(attendance_absent_count)
    
    context={
        # "total_attendance": total_attendance,
        # "attendance_present": attendance_present,
        # "attendance_absent": attendance_absent,
        # "total_subjects": total_subjects,
        "subject_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent
    }
    return render(request, "student_template/student_home_template.html", context)

def enroll_session(request):
    enrollments = Session.objects.all()

    context = {
        "enrollments":enrollments,
        # "enrolled_enrollments":enrolled_enrollments
    }
    return render(request, "student_template/student_enrollment_management.html", context)

#TODO: FIX THIS FREAKING DISASTER
def enroll_session_save(request,enrollment_id):
    enrollment = Session.objects.get(id=enrollment_id)
    enrollments = Session.objects.all()
    student = Students.objects.get(admin=request.user.id)
    # enrolled_enrollments = Enrollment.objects.get(student=Students.objects.get(admin=request.user))

    context = {
        "enrollments":enrollments,
        # "enrolled_enrollments":enrolled_enrollments
    }

    try:
        if created := Enrollment.objects.get(student=student, session=enrollment):
            messages.info(request, "You are already Succesfully enrolled")
            print(created)
            context = {
                "enrollments":enrollments,
                "try": created
            }
            return render(request, "student_template/student_enrollment_management.html", context)

        elif created := Enrollment.objects.get_or_create(student=student, session=enrollment):
            messages.success(request, "Succesfully enrolled")
        else:
            messages.info(request, "You are already Succesfully enrolled")
        return render(request, "student_template/student_enrollment_management.html", context)
    except Exception as e:
        messages.error(request, f"Not Succesfully enrolled, because {e}")
        return render(request, "student_template/student_enrollment_management.html", context)

    # return render(request, "student_template/student_enrollment_management.html", context)


def enroll_classes(request):
    classes_all = Class.objects.all()
    student = Students.objects.get(admin=request.user.id)
    list_of_classes = ClassEnrollment.objects.filter(student_id=student.id)
    print(list_of_classes)
    compulsory_classes = [i.selected_class for i in list_of_classes]
    classes = [i for i in classes_all if i not in compulsory_classes]
    context = {
        'classes':classes,
        'compulsory_classes':compulsory_classes
    }
    return render(request, "student_template/class_enrollment_management.html", context)


def enroll_class_save(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        class_id = Class.objects.get(id=class_id)
        print(class_id)
        student = Students.objects.get(admin=request.user.id)
        enroll = ClassEnrollment(student=student,selected_class=class_id)
        try:
            
            enroll.save()
            print(enroll)
            # return JsonResponse({'success': True}, status=200)
            return redirect('enroll_classes')
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=405)
        
    return JsonResponse({'success': False}, status=405)
        # return render(request, "student_template/class_enrollment_management.html")
    

def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'student_template/student_apply_leave.html', context)


def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('student_apply_leave')


def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student_template/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Students.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student_id=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)

    context={
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
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

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


def student_view_result(request):
    student = Students.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student.id)
    context = {
        "student_result": student_result,
    }
    return render(request, "student_template/student_view_result.html", context)


def students_sessions_management(request):
    student = Students.objects.get(admin=request.user.id)
    deferrement_approval_workflow_form = DefferementApprovalWorkflowForm()
    temporary_withdrawal_workflow_form = TemporaryWithdrawalApprovalWorklowForm()
    student_deffer_status = check_student_is_defferred(student)
    student_temporary_withdrawal_status = check_student_is_temporarily_withdrawn(student)

    context = {
        "deferrement_approval_workflow_form": deferrement_approval_workflow_form,
        "temporary_withdrawal_workflow_form":temporary_withdrawal_workflow_form,
        "student_deffer_status":student_deffer_status,
        "student_temporary_withdrawal_status":student_temporary_withdrawal_status

    }
    return render(request, "student_template/student_session_management.html", context)


def defer_student(request):
    reason = request.POST.get('reason')
    student = Students.objects.get(admin=request.user.id)

    try:
        defer_obj = DeferrmentApprovalWorklow.objects.create(
            applicant = student,
            reason = reason
        )
        defer_obj.save()
        messages.success(request,'Application for deferrment made')
        return render(request, "student_template/student_session_management.html")
    except Exception as e:
        messages.error(request,f'{e}')
        return render(request, "student_template/student_session_management.html")

def withdraw_student(request):
    reason = request.POST.get('reason')
    student = Students.objects.get(admin=request.user.id)

    try:
        defer_obj = TemporaryWithdrawalApprovalWorklow.objects.create(
            applicant = student,
            reason = reason
        )
        defer_obj.save()
        messages.success(request,'Application for deferrment made')
        return render(request, "student_template/student_session_management.html")
    except Exception as e:
        messages.error(request,f'{e}')
        return render(request, "student_template/student_session_management.html")
    

def student_housing(request):

    houses = House.objects.all()
    student = Students.objects.get(admin=request.user.id)
    
    print(student)
    context = {
        "houses":houses,
        "student":student,
    }
    
    return render(request, "student_template/student_housing_template.html", context)


def book_housing(request, house_id):
    house = House.objects.get(id=house_id)
    student = Students.objects.get(admin=request.user.id)
    
    try:
        if student.booked_hostel:
            messages.warning(request, "You have already booked a house, kindly wait for a response")
            print(student)
            return redirect('student_housing')
        else:
            house.student = student
            house.current_capacity += 1
            student.booked_hostel = True
            house.save()
            student.save()

            # Check if the student has already booked a house
            if Booking.objects.filter(student=student, status=True).exists():
                messages.warning(request, "You have already booked a house.")
                return redirect('student_housing')  # Adjust the URL name as per your project
            
            # Create a new booking entry
            booking = Booking.objects.create(
                student=student,
                house=house,
                booking_date=timezone.now().date(), # type: ignore
                # Assuming 'Session' model is defined in your 'academics' app
                session=Session.objects.get(pk=1),  # Adjust the session as needed
            )
            
            messages.success(request, "Booking successful!")
            print('house booked')
            messages.success(request, "Successfully Booked")
            return redirect('student_housing')
    except Exception as e:
        print('house not booked')
        messages.error(request, f"Failed to Book {e}")
        return redirect('student_housing')
    
