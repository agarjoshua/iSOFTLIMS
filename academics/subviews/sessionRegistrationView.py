from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from academics.forms.sessionforms import EnrollmentCreateForm
from academics.models import Enrollment, Session
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from core.subviews.utilities.accesscontrolutilities import allow_user
from django.contrib.admin.views.decorators import user_passes_test

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
@allow_user('1','4','6') 
def manage_session_registation(request):
    currently_enrolled = Enrollment.objects.filter(Q(session__is_current=True))
    print(currently_enrolled)
    # currently_enrolled = Enrollment.objects.all()
    context = {
        "currently_enrolled" : currently_enrolled
        }
    return render(request, "session_templates/manage_session_registration_template.html", context)

@user_passes_test(is_admin)
@allow_user('1','4','6') 
def enroll_student(request):
    if request.method == 'POST':
        form = EnrollmentCreateForm(request.POST)
        if form.errors:
            form_errors = form.errors
            form_errors = str(form_errors)
            start_index = form_errors.find('<li>') + len('<li>')
            end_index = form_errors.find('</li>', start_index)
            li_message = form_errors[start_index:end_index]

            start_index = li_message.find('<li>') + len('<li>')
            end_index = li_message.find('</li>', start_index)
            message = li_message[start_index:end_index]
            messages.warning(request, f'Cannot enroll because - {message}')
            redirect('academics:enroll_student')
        if form.is_valid():
            print(form.errors)
            try:
                form.save()
                messages.success(request, 'Student Succesfully Enrolled')
                return redirect('academics:manage_session_registation')
            except Exception as e:
                print(e)
                messages.error(request, f'an error occurred {e}')
            # return redirect('manage_session_registation')
        else:
            form = EnrollmentCreateForm()
    form = EnrollmentCreateForm()
    return render(request, 'session_templates/enroll_student_template.html', {'form': form})

@user_passes_test(is_admin)
@allow_user('1','4','6') 
def confirm_enrollment(request,enrolled_id):
    selected_enrollment= Enrollment.objects.get(id=enrolled_id)
    return render(request, 'session_templates/enroll_student_template.html', {'form': form})


@require_POST
# @csrf_exempt
def mass_edit_enrolled(request):
    enrolled_ids = request.POST.getlist('enrolled_ids[]')
    
    for i in enrolled_ids:
        print(i)
        currently_enrolled = Enrollment.objects.filter(id=i)
        currently_enrolled.update(is_active=True)
        print(currently_enrolled)

    return redirect('academics:manage_session_registation')

@user_passes_test(is_admin)
@allow_user('1','4','6') 
def revoke_enrollment(request, enrolled_id):
    revoked_enrollment = Enrollment.objects.get(id=enrolled_id)
    revoked_enrollment.is_active = False
    revoked_enrollment.save()
    messages.warning(request, 'Student succesfully deregistered from semester')
    return redirect('academics:manage_session_registation')