from django.shortcuts import render, redirect
from academics.models import Exam
from academics.forms.examforms import ExamForm


def manage_examinations(request):
    exams = Exam.objects.all()
    form = ExamForm()
    context = {'exams': exams, 'form': form}
    return render(request, 'exam_templates/manage_examinations_template.html')