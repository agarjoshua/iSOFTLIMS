from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from academics.forms.classforms import ClassEditForm, ClassCreateForm
from academics.forms.gradeforms import ClassGradeForm, GradeEditForm
from academics.models import Class, Grade

from django.views.decorators.csrf import csrf_exempt

#########################################MANAGE  COURSES#######################################################################

def add_class(request):
    form = ClassCreateForm()
    context = {"form": form}
    return render(request, "admin_template/add_class_template.html", context)                


def add_class_save(request):
    if request.method == 'POST':
        form = ClassCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Class Succesfully Added")
            return redirect("add_class")
    else:
        messages.error(request, "Invalid Method!")
        form = ClassCreateForm()
    render (request, "admin_template/manage_class_template.html", {'form': form})



def manage_class(request):
    classs = Class.objects.all()
    context = {"classs": classs}
    return render(request, "admin_template/manage_class_template.html", context)


def edit_class(request, class_id):
    selected_class = Class.objects.get(id=class_id)
    if request.method == 'POST':
        form = ClassEditForm(request.POST, instance=selected_class)
        if form.is_valid():
            try: 
                form.save()
                messages.success(request, "Class edited Successfully.")
                return redirect('edit_class', class_id=class_id)
            except Exception as e:
                messages.error(request, f"Failed to Edit Class. bacause {e}")
                form = ClassEditForm(instance=selected_class)

        else:
            messages.error(request, "Failed to Edit Class. Form isnt valid")
            return _edit_class_helper(selected_class, class_id, request)
    else:
        _edit_class_helper(selected_class, class_id, request)

    return _edit_class_helper(selected_class, class_id, request)

def _edit_class_helper(selected_class, class_id, request):
    form = ClassEditForm(instance=selected_class)
    context = {'form': form, 'selected_class': selected_class, "id": class_id}
    return render(request, "admin_template/edit_class_template.html", context)



def delete_class(request, class_id):
    selected_class = Class.objects.get(id=class_id)
    try:
        selected_class.delete()
        messages.success(request, "Class Deleted Successfully.")
        return redirect("manage_class")
    except:
        messages.error(request, "Failed to Delete Class.")
        return redirect("manage_class")
    


def manage_grade(request):
    grade = Grade.objects.all()
    context = {"grades": grade}
    return render(request, "admin_template/manage_grade_template.html", context)

def add_grade(request):
    form = ClassGradeForm()
    context = {"form": form}
    return render(request, "admin_template/add_grade_template.html", context)               

def add_grade_save(request):
    if request.method == 'POST':
        form = ClassGradeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Grade Succesfully Added")
            return redirect("add_grade")
    else:
        messages.error(request, "Invalid Method!")
        form = ClassGradeForm()
    render (request, "admin_template/manage_grade_template.html", {'form': form})

def edit_grade(request, grade_id):
    selected_grade = Grade.objects.get(id=grade_id)
    if request.method == 'POST':
        form = GradeEditForm(request.POST, instance=selected_grade)
        if form.is_valid():
            try: 
                form.save()
                messages.success(request, "Grade edited Successfully.")
                return redirect('edit_grade', grade_id=grade_id)
            except Exception as e:
                messages.error(request, f"Failed to Edit Grade. bacause {e}")
                form = GradeEditForm(instance=selected_grade)

        else:
            messages.error(request, "Failed to Edit Grade. Form isnt valid")
            return _edit_grade_helper(selected_grade, grade_id, request)
    else:
        _edit_grade_helper(selected_grade, grade_id, request)

    return _edit_grade_helper(selected_grade, grade_id, request)

def _edit_grade_helper(selected_grade, grade_id, request):
    form = ClassGradeForm(instance=selected_grade)
    context = {'form': form, 'selected_grade': selected_grade, "id": grade_id}
    return render(request, "admin_template/edit_grade_template.html", context)


def delete_grade(request, grade_id):
    selected_grade = Grade.objects.get(id=grade_id)
    try:
        selected_grade.delete()
        messages.success(request, "Grade Deleted Successfully.")
        return redirect("manage_grade")
    except Exception as e:
        messages.error(request, f"Failed to Delete Grade, because {e}")
        return redirect("manage_grade")

# TODO: Fix this disaster
@csrf_exempt
def check_class_exist(request):
    class_name = request.POST.get("class_name")
    if selected_class := Class.objects.filter(class_name=class_name).exists():
        return HttpResponse(True)
    else:
        return HttpResponse(False)