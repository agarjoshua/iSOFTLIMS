from django.shortcuts import render, redirect
from academics.models import Exam, ExamType, GradeLevel, GradeRange
from academics.forms.examforms import ExamForm, ExamTypeForm, GradeRangeForm
from django.contrib import messages
from django.core.exceptions import ValidationError

def manage_examinations(request):
    
    # FORMS
    exam_form = ExamForm()
    exam_type_form = ExamTypeForm()
    grade_range_form = GradeRangeForm()

    # LISTS
    exams = Exam.objects.all()
    exam_type_list = ExamType.objects.all()
    grade_range_list = GradeRange.objects.all()
    print(grade_range_list)

    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request,'Exam type ADDED Succesfully')
                return redirect('manage_exams')
            except Exception as e:
                messages.error(request,f'Exam type NOT Added Succesfully bacuse - {e}')
                return redirect('manage_exams')

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
                return redirect('manage_exams')
            except Exception as e:
                messages.error(request,f'Exam type NOT Added Succesfully bacuse - {e}')
                return redirect('manage_exams')

            
def add_grade(request):
    if request.method == 'POST':
        grade = request.POST.get('grade')
        min_score = int(request.POST.get('min_score'))
        max_score = int(request.POST.get('max_score'))
        exam_id = request.POST.get('exam_id')

        exam = Exam.objects.get(id=exam_id) 
        if grade_ranges:=GradeRange.objects.filter(exam=exam, grade=grade).exists():
            messages.error(request,'This grade already exists for this exam')
            return redirect('manage_exams')

        grade_ranges = GradeRange.objects.filter(exam=exam).order_by('min_score', 'max_score')
        prev_grade_range = None
        for grade_range in grade_ranges:
            if prev_grade_range and (min_score <= prev_grade_range.max_score or max_score <= grade_range.min_score):
                # overlapping score range, return error response
                messages.error(request,'The score range overlaps with an existing grade for this exam')
                return redirect('manage_exams')
            prev_grade_range = grade_range

        grade_range = GradeRange(exam=exam, grade=grade, min_score=min_score, max_score=max_score)
        grade_range.save()

        
        return redirect('manage_exams')

def add_new_grade(request):
    if request.method == 'POST':
        grade = request.POST.get('grade')
        min_score = int(request.POST.get('min_score'))
        max_score = int(request.POST.get('max_score'))
        exam_id = request.POST.get('exam_id')

        exam = Exam.objects.get(id=exam_id) 
        if grade_ranges:=GradeRange.objects.filter(exam=exam, grade=grade).exists():
            messages.error(request,'This grade already exists for this exam')
            return redirect('manage_exams')

        grade_ranges = GradeRange.objects.filter(exam=exam).order_by('min_score', 'max_score')
        prev_grade_range = None
        for grade_range in grade_ranges:
            if prev_grade_range and (min_score <= prev_grade_range.max_score or max_score <= grade_range.min_score):
                # overlapping score range, return error response
                messages.error(request,'The score range overlaps with an existing grade for this exam')
                return redirect('manage_exams')
            prev_grade_range = grade_range

        grade_range = GradeRange(exam=exam, grade=grade, min_score=min_score, max_score=max_score)
        grade_range.save()

        
        return redirect('manage_exams')