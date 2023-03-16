from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from academics.forms.classforms import ClassForm
from academics.models import Class

from django.views.decorators.csrf import csrf_exempt

#########################################MANAGE  COURSES#######################################################################

def add_class(request):
    form = ClassForm()
    context = {"form": form}
    return render(request, "admin_template/add_class_template.html", context)                


def add_class_save(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Class Succesfully Added")
            return redirect("add_class")
    else:
        messages.error(request, "Invalid Method!")
        form = ClassForm()
    render (request, "admin_template/manage_class_template.html", {'form': form})



def manage_class(request):
    classs = Class.objects.all()
    context = {"classs": classs}
    return render(request, "admin_template/manage_class_template.html", context)


def edit_class(request, class_id):
    selected_class = Class.objects.get(id=class_id)
    context = {"class": selected_class, "id": class_id}
    return render(request, "admin_template/edit_class_template.html", context)


def edit_class_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        class_id = request.POST.get("class_id")
        class_name = request.POST.get("class")
        cost = request.POST.get("class")

        try:
            selected_class = Class.objects.get(id=class_id)
            selected_class.class_name = class_name
            selected_class.cost = cost
            selected_class.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect("/edit_class/" + class_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect("/edit_class/" + class_id)


def delete_class(request, class_id):
    selected_class = Class.objects.get(id=class_id)
    try:
        selected_class.delete()
        messages.success(request, "Course Deleted Successfully.")
        return redirect("manage_class")
    except:
        messages.error(request, "Failed to Delete Course.")
        return redirect("manage_class")
    


@csrf_exempt
def check_class_exist(request):
    class_name = request.POST.get("class_name")
    if class_obj := Class.objects.filter(class_name=class_name).exists():
        return HttpResponse(True)
    else:
        return HttpResponse(False)