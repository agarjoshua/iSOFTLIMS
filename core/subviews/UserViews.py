from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages

from core.models import Applicant, CustomUser, Department, Staff, Students, Teacher
from academics.models import Course, Enrollment, Session, Exam
from finance.models import Transaction



def user_home(request):

    # admin
    users = CustomUser.objects.all()
    teacher_count = Teacher.objects.count()
    staff_count = Staff.objects.count()
    student_count = Students.objects.count()
    current_session = Session.objects.get(is_current=True)
    user = request.user

    # academics
    applicants_count = Applicant.objects.count()


    # finance 
    transactions_count = Transaction.objects.filter(confirmed=False).count()

    # learning
    session_enrollment_count = Enrollment.objects.count()
    course_count = Course.objects.count()
    departments = Department.objects.count()

    #examinations
    exam_count = Exam.objects.count()


    context = {
        "users": users,
        "user": user,
        "teacher_count": teacher_count,
        "staff_count": staff_count,
        "student_count": student_count,
        "current_session": current_session,
        "applicants_count": applicants_count,
        "transactions_count": transactions_count,
        "session_enrollment_count": session_enrollment_count,
        "exam_count": exam_count,
        "course_count": course_count,
        "departments": departments
    }
    return render(request, "user_home.html", context)