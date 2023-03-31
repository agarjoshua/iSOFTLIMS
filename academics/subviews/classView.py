from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from academics.forms.classforms import ClassEditForm, ClassCreateForm
from academics.forms.clusterforms import ClusterClassForm
from academics.forms.gradeforms import ClassGradeForm, GradeEditForm
from academics.models import Class, ClusterClass, GradeLevel
from django.views.decorators.csrf import csrf_exempt



def add_class(request):
    form = ClassCreateForm()
    if request.method == 'POST':
        form = ClassCreateForm(request.POST)

        try:
            if form.is_valid():
                form.save()
                form = ClassCreateForm()
                context = {
                    'form': form
                }
                messages.success(request, "Class Succesfully Added")
                render (request, "admin_template/add_class_template.html", context)
            errors = None if form.is_valid() else form.errors.as_data()
            context = {
                'errors': errors,
                'form': form
                }
            render (request, "admin_template/add_class_template.html", context)
        except Exception as e:
            messages.error(request, f"This class was NOT added -- {e}")
            return redirect("add_class")
    else:
        form = ClassCreateForm()
    return render (request, "admin_template/add_class_template.html", {'form': form})
    

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
    grade = GradeLevel.objects.all()
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
    selected_grade = GradeLevel.objects.get(id=grade_id)
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
    selected_grade = GradeLevel.objects.get(id=grade_id)
    try:
        selected_grade.delete()
        messages.success(request, "Grade Deleted Successfully.")
        return redirect("manage_grade")
    except Exception as e:
        messages.error(request, f"Failed to Delete Grade, because {e}")
        return redirect("manage_grade")


def clusterclass_list(request):
    clusters = ClusterClass.objects.all()
    classes = Class.objects.all()
    context = {
        "clusters": clusters,
        "classes": classes
        }
    return render(request, "admin_template/manage_clusters_template.html", context)

def clusterclass_detail(request, pk):
    clusterclass = get_object_or_404(ClusterClass, pk=pk)
    return render(request, 'admin_template/clusterclass_detail.html', {'clusterclass': clusterclass})


def clusterclass_create(request):
    # sourcery skip: extract-duplicate-method, extract-method
    if request.method == 'POST':
        form = ClusterClassForm(request.POST)
        if form.is_valid():
            cluster_class_name = request.POST.get('cluster_class_name')
            class_ids = request.POST.getlist('classes')

            # Create a new ClusterClass instance and save it to the database
            clusterclass, _ = ClusterClass.objects.get_or_create(cluster_class_name=cluster_class_name)
            clusterclass.classes.set(class_ids)
            print('----------------------------------')
            print(f'the clusterclass name is - {clusterclass}')
            print('----------------------------------')
            print(class_ids)
            # clusterclass.save()
            try:
                clusterclass.classes.set(class_ids)
                messages.success(request,' I guess it works?')
                return redirect('clusterclass_list')
            except Exception as e:
                messages.error(request,e)
                print(e)
                return redirect('clusterclass_list')
    else:
        form = ClusterClassForm()
    return render(request, 'admin_template/add_clusterclass_template.html', {'form': form})



 # Add Class objects to the ClusterClass instance's many-to-many field
            # for class_id in class_ids:
            #     try:
            #         class_instance = Class.objects.get(pk=int(class_id))
            #         print('----------------------------------')
            #         print(f'the class instance name is - {class_instance}')
            #         print('----------------------------------')

            #         # clusterclass.classes.add(class_instance)
            #         clusterclass.classes.set(class_instance)

            #         print('----------------------------------')
            #         # print(f'the clusterclass before updated - {clusterclass.classes.set(class_ids)}')
            #         print('----------------------------------')
                

            #         print('----------------------------------')
            #         print(f'the clusterclass updated is is - {clusterclass}')
            #         print('----------------------------------')
            #     except Exception as e:
            #         # Handle invalid class IDs
            #         # clusterclass.delete()
            #         print(e)
            #         return HttpResponseBadRequest(e)

            # return redirect('clusterclass_detail', pk=clusterclass.pk)


def clusterclass_edit(request,clusterclass_id):
    clusterclass = get_object_or_404(ClusterClass, id=clusterclass_id)
    if request.method == 'POST':
        form = ClusterClassForm(request.POST, instance=clusterclass)
        if form.is_valid():
            clusterclass = form.save()
            ClusterClassForm(instance=clusterclass)
            messages.success(request,'Cluster Class Updated Succesfully')
            return render(request, 'admin_template/edit_clusterclass_template.html', {'form': form})
    else:
        form = ClusterClassForm(instance=clusterclass)
    return render(request, 'admin_template/edit_clusterclass_template.html', {'form': form})



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