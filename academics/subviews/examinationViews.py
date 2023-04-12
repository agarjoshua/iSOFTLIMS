from django.shortcuts import render, redirect
from academics.models import Exam, ExamType, GradeRange
from academics.forms.examforms import ExamForm, ExamTypeForm, GradeRangeForm
from django.contrib import messages

def manage_examinations(request):
    
    # FORMS
    exam_form = ExamForm()
    exam_type_form = ExamTypeForm()
    grade_range_form = GradeRangeForm()

    # LISTS
    exams = Exam.objects.all()
    exam_type_list = ExamType.objects.all()
    grade_range_list = GradeRange.objects.all()

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