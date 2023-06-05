from django import template
from django.shortcuts import render, redirect, get_object_or_404
from academics.models import Class, ClassEnrollment, ClusterClass, Exam, ExamRegistration, ExamType, GradeLevel, GradeRange
from academics.forms.examforms import ExamForm, ExamTypeForm, GradeRangeForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from core.models import Students

from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.http import JsonResponse

from django.middleware import csrf

import pudb
def manage_examinations(request):
    
    # FORMS
    exam_form = ExamForm()
    exam_type_form = ExamTypeForm()
    grade_range_form = GradeRangeForm()

    # LISTS
    exams = Exam.objects.all()
    exam_type_list = ExamType.objects.all()
    grade_range_list = GradeRange.objects.all()

    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                # pudb.set_trace()
                messages.success(request,'Exam type ADDED Succesfully')
                return redirect('academics:manage_exams')
                
            except Exception as e:
                messages.error(request,f'Exam type NOT Added Succesfully bacuse - {e}')
                return redirect('academics:manage_exams')

    context = {
        "exam": exams, 
        "exam_form": exam_form,
        "exam_type_form": exam_type_form,
        "exam_type_list": exam_type_list,
        "grade_range_form":grade_range_form,
        "grade_range_list": grade_range_list,
        }
    return render(request, "exam_templates/manage_examinations_template.html", context)

def add_exam_type(request):
    if request.method == 'POST':
        form = ExamTypeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request,'Exam type ADDED Succesfully')
                return redirect('academics:manage_exams')
            except Exception as e:
                messages.error(request,f'Exam type NOT Added Succesfully bacuse - {e}')
                return redirect('academics:manage_exams')

            
def add_grade(request):
    if request.method == 'POST':
        grade = request.POST.get('grade')
        min_score = int(request.POST.get('min_score'))
        max_score = int(request.POST.get('max_score'))
        exam_id = request.POST.get('exam_id')

        exam = Exam.objects.get(id=exam_id) 
        if grade_ranges:=GradeRange.objects.filter(exam=exam, grade=grade).exists():
            messages.error(request,'This grade already exists for this exam')
            return redirect('academics:manage_exams')

        grade_ranges = GradeRange.objects.filter(exam=exam).order_by('min_score', 'max_score')
        prev_grade_range = None
        for grade_range in grade_ranges:
            if prev_grade_range and (min_score <= prev_grade_range.max_score or max_score <= grade_range.min_score):
                # overlapping score range, return error response
                messages.error(request,'The score range overlaps with an existing grade for this exam')
                return redirect('academics:manage_exams')
            prev_grade_range = grade_range

        grade_range = GradeRange(exam=exam, grade=grade, min_score=min_score, max_score=max_score)
        grade_range.save()

        
        return redirect('academics:manage_exams')

def add_new_grade(request):
    if request.method == 'POST':
        grade = request.POST.get('grade')
        min_score = int(request.POST.get('min_score'))
        max_score = int(request.POST.get('max_score'))
        exam_id = request.POST.get('exam_id')

        exam = Exam.objects.get(id=exam_id) 
        if grade_ranges:=GradeRange.objects.filter(exam=exam, grade=grade).exists():
            messages.error(request,'This grade already exists for this exam')
            return redirect('academics:manage_exams')

        grade_ranges = GradeRange.objects.filter(exam=exam).order_by('min_score', 'max_score')
        prev_grade_range = None
        for grade_range in grade_ranges:
            if prev_grade_range and (min_score <= prev_grade_range.max_score or max_score <= grade_range.min_score):
                # overlapping score range, return error response
                messages.error(request,'The score range overlaps with an existing grade for this exam')
                return redirect('academics:manage_exams')
            prev_grade_range = grade_range

        grade_range = GradeRange(exam=exam, grade=grade, min_score=min_score, max_score=max_score)
        grade_range.save()

        
        return redirect('academics:manage_exams')
    

def register_for_exam(request):
    # student model has grade, we pick the subjects from the gradelevel
    if student := Students.objects.get(admin=request.user.id):
        # list_of_classes = ClusterClass.objects.get(id=test.id)
        # list_of_classes = list_of_classes.classes.all()
        # list_of_classes_id = [i.id for i in list_of_classes]
        # # registered_classes = 

        # print([i.id for i in list_of_classes])
        # assume `student` is the given `Students` instance
        # retrieve all class enrollments of the student
        class_enrollments = ClassEnrollment.objects.filter(student=student)

        # retrieve all exams related to the enrolled classes
        exams = Exam.objects.filter(exam_class__in=[ce.selected_class for ce in class_enrollments])

        exam = Exam.objects.all()
        enrollments = ClassEnrollment.objects.filter(student=student)

        # registered_exams = ExamRegistration.objects.filter(student=student)

        exam_list = ExamRegistration.objects.filter(student=student, registered=True)
        registered_exams = [exam.exams for exam in exam_list]
        print(f'enrollments are{enrollments}')

        # registered_exams = [enrollment.selected_class.exam_set.all() for enrollment in enrollments]
        print(f'registered exams -  {registered_exams}')



    else:
        messages.warning(request,'Student is not registered to any class')
        return render(request, "student_template/student_register_exams_template.html")

    return render(
        request, 
        "student_template/student_register_exams_template.html", 
        {
            'classes':exams,
            'student':student,
            'class_enrollments': class_enrollments,
            'registered_exams':registered_exams
         })


@require_POST
def mass_edit_student_exam(request):

    registered_ids = request.POST.getlist('registered_ids[]')

    for i in registered_ids:
        
        exam = Exam.objects.get(id=i)
        print(f'the exam is {exam}')
        student = Students.objects.get(admin=request.user.id)
        exam_reg = ExamRegistration(exams=exam,student=student,registered=True)
        exam_reg.save()

    if student := Students.objects.get(admin=request.user.id):
        list_of_classes = ClusterClass.objects.get(id=student.id)
        print(list_of_classes)
        classes = list_of_classes.classes.all()

        # Retrieve all the approved and registered ExamRegistration objects for the student
        exam_registrations = ExamRegistration.objects.filter(student=student, approved=True, registered=True)

        # Create an empty list to store the exams
        exams_list = []

        # Iterate through the ExamRegistration objects and extract the corresponding exam objects
        for registration in exam_registrations:
            exams_list.append(registration.exams)

        return redirect('academics:register_for_exam')

        # context = {
        #     'classes': classes,
        #     'exam_list': exams_list

        # }

        # table_html = render_to_string('student_template/student_register_exams_template.html', context)

        # return JsonResponse({'table_html': table_html})