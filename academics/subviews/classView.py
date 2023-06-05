from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from academics.forms.classforms import ClassEditForm, ClassCreateForm
from academics.forms.clusterforms import ClusterClassForm
from academics.forms.gradeforms import ClassGradeForm, GradeEditForm
from academics.models import Class, ClusterClass, GradeLevel
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import user_passes_test


def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def add_class(request):
    # form = ClassCreateForm()
    if request.method == 'POST':
        form = ClassCreateForm(request.POST)
        try:
            if form.is_valid():
                class_name = request.POST.get('class_name')
                if Class.objects.filter(class_name=class_name).exists():
                    messages.error(request, 'A class with this name already exists')
                else:
                    form.save()
                    messages.success(request, "Class Succesfully Added")
                    return redirect('academics:manage_class')
            errors = None if form.is_valid() else form.errors.as_data()
            context = {
                'errors': errors,
                'form': form
                }
            render (request, "class_templates/add_class_template.html", context)
        except Exception as e:
            messages.error(request, f"This class was NOT added -- {e}")
            return redirect("academics:add_class")
    else:
        form = ClassCreateForm()
    return render (request, "class_templates/add_class_template.html", {'form': form})
    
@user_passes_test(is_admin)
def manage_class(request):
    classs = Class.objects.all()
    context = {"classs": classs}
    return render(request, "class_templates/manage_class_template.html", context)

@user_passes_test(is_admin)
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
    return render(request, "class_templates/edit_class_template.html", context)


@user_passes_test(is_admin)
def delete_class(request, class_id):
    selected_class = Class.objects.get(id=class_id)
    try:
        selected_class.delete()
        messages.success(request, "Class Deleted Successfully.")
        return redirect("academics:manage_class")
    except:
        messages.error(request, "Failed to Delete Class.")
        return redirect("academics:manage_class")
    



@user_passes_test(is_admin)
def manage_grade(request):
    grade = GradeLevel.objects.all()
    context = {"grades": grade}
    return render(request, "class_templates/manage_grade_template.html", context)

@user_passes_test(is_admin)
def add_grade(request):
    form = ClassGradeForm()
    context = {"form": form}
    return render(request, "class_templates/add_grade_template.html", context)  
             
@user_passes_test(is_admin)
def add_grade_save(request):
    if request.method == 'POST':
        form = ClassGradeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Grade Succesfully Added")
            return redirect("academics:manage_grade")
    else:
        messages.error(request, "Invalid Method!")
        form = ClassGradeForm()
    render (request, "class_templates/manage_grade_template.html", {'form': form})

@user_passes_test(is_admin)
def edit_grade(request, grade_id):
    selected_grade = GradeLevel.objects.get(id=grade_id)
    if request.method == 'POST':
        form = GradeEditForm(request.POST, instance=selected_grade)
        if form.is_valid():
            try: 
                form.save()
                messages.success(request, "Grade edited Successfully.")
                return redirect("academics:manage_grade")
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
    return render(request, "class_templates/edit_grade_template.html", context)

@user_passes_test(is_admin)
def delete_grade(request, grade_id):
    selected_grade = GradeLevel.objects.get(id=grade_id)
    try:
        selected_grade.delete()
        messages.success(request, "Grade Deleted Successfully.")
        return redirect("academics:manage_grade")
    except Exception as e:
        messages.error(request, f"Failed to Delete Grade, because {e}")
        return redirect("academics:manage_grade")

@user_passes_test(is_admin)
def clusterclass_list(request):
    clusters = ClusterClass.objects.all()
    classes = Class.objects.all()
    context = {
        "clusters": clusters,
        "classes": classes
        }
    return render(request, "class_templates/manage_clusters_template.html", context)

@user_passes_test(is_admin)
def clusterclass_detail(request, pk):
    clusterclass = get_object_or_404(ClusterClass, pk=pk)
    return render(request, 'class_templates/clusterclass_detail.html', {'clusterclass': clusterclass})

@user_passes_test(is_admin)
def clusterclass_create(request):  # sourcery skip: extract-method
    if request.method == 'POST':
        form = ClusterClassForm(request.POST)
        if form.is_valid():
            cluster_class_name = request.POST.get('cluster_class_name')
            class_ids = request.POST.getlist('classes')
            # Create a new ClusterClass instance and save it to the database
            clusterclass, _ = ClusterClass.objects.get_or_create(cluster_class_name=cluster_class_name)
            clusterclass.classes.set(class_ids)
            messages.success(request,'Cluster Class Added Succesfully')
            return redirect('academics:clusterclass_list')
    else:
        form = ClusterClassForm()
    return render(request, 'class_templates/add_clusterclass_template.html', {'form': form})


@user_passes_test(is_admin)
def clusterclass_edit(request,clusterclass_id):
    clusterclass = get_object_or_404(ClusterClass, id=clusterclass_id)
    if request.method == 'POST':
        form = ClusterClassForm(request.POST, instance=clusterclass)
        if form.is_valid():
            clusterclass = form.save()
            ClusterClassForm(instance=clusterclass)
            messages.success(request,'Cluster Class Updated Succesfully')
            return redirect('academics:clusterclass_list')
    else:
        form = ClusterClassForm(instance=clusterclass)
    return render(request, 'class_templates/edit_clusterclass_template.html', {'form': form})



# TODO: Fix this disaster
@csrf_exempt
def check_class_exist(request):
    class_name = request.POST.get("class_name")
    if selected_class := Class.objects.filter(class_name=class_name).exists():
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    
@csrf_exempt
def check_cluster_class_exist(request):
    class_name = request.POST.get('cluster_class_name')
    if selected_class := ClusterClass.objects.filter(cluster_class_name=class_name).exists():
        return HttpResponse(True)
    else:
        return HttpResponse(False)