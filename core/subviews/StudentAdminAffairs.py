from django.shortcuts import render, redirect
from core.forms.approvalforms import AdminDefferementApprovalWorkflowForm, InterFacultyTransferWorkflowForm, TemporaryDefferementApprovalWorkflowForm
from django.contrib import messages
from core.models import HOD, DeferrmentApprovalWorklow, InterFacultyTransferApprovalWorklow, Students, TemporaryWithdrawalApprovalWorklow
from core.subviews.utilities.StudentViewUtilities import check_hod_type
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


def student_affairs_home(request):
    deffereals_count = DeferrmentApprovalWorklow.objects.count()
    temp_defer_count = TemporaryWithdrawalApprovalWorklow.objects.count()
    interfacultytransfer_count = InterFacultyTransferApprovalWorklow.objects.count()
    all_student_count = Students.objects.all().count()
    students = Students.objects.all()
    context = {
        "deffereals_count":deffereals_count,
        "temp_defer_count":temp_defer_count,
        "interfacultytransfer_count":interfacultytransfer_count,
        "all_student_count":all_student_count,
        "students": students
            }
    return render(request, "admin_template/manage_student_admin_affairs.html", context)


def manage_student_approvals(request):
    approvals = DeferrmentApprovalWorklow.objects.all()
    deferrement_approval_workflow_form = AdminDefferementApprovalWorkflowForm()
    try:
        role = HOD.objects.get(admin=request.user.id).hod_type
        context = {
            "approvals":approvals,
            "deferrement_approval_workflow_form":deferrement_approval_workflow_form,
            "role":role
        }
        return render(request, "admin_template/manage_student_approvals.html", context)
    except ObjectDoesNotExist:
        not_authorized = True
        context = {
            "approvals":approvals,
            "deferrement_approval_workflow_form":deferrement_approval_workflow_form,
            # "not_authorized": not_authorized
            # "role":role
        }
        return render(request, "admin_template/manage_student_approvals.html", context)

def confirm_defer_student(request):  # sourcery skip: avoid-builtin-shadow
    id = request.POST.get('id')
    comments = request.POST.get('comments')

    print(f'comments - [{comments}]')
    print(id)
    print(request.user)

    # try:
    role = HOD.objects.get(admin=request.user.id).hod_type
    print(role)
    defer_obj = DeferrmentApprovalWorklow.objects.get(id=id)
    print(defer_obj)
    if role.name == 'Admissions':
        defer_obj.admissions_comments = comments
        defer_obj.admissions_approved = True
        defer_obj.save()
    elif role.name == 'Dean':
        defer_obj.dean_comments = comments
        defer_obj.dean_approved = True
        defer_obj.save()
    elif role.name == 'Registrar':
        defer_obj.registrar_comments = comments
        defer_obj.registrar_approved = True
        defer_obj.save()
    elif role.name == 'DVC':
        defer_obj.dvc_comments = comments
        defer_obj.dvc_approved = True
        defer_obj.applicant.academic_status = 2
        print(defer_obj.applicant)
        print(defer_obj.applicant.academic_status)
        defer_obj.save()
    messages.success(request,'Application for deferrment made')
    return redirect("manage_student_approvals")

def deny_defer_student(request):
    id = request.POST.get('id')
    comments = request.POST.get('comments')

    print(f'comments - [{comments}]')
    print(id)
    print(request.user)

    # try:
    role = HOD.objects.get(admin=request.user.id).hod_type
    print(role)
    defer_obj = DeferrmentApprovalWorklow.objects.get(id=id)
    print(defer_obj)
    if role.name == 'Admissions':
        defer_obj.admissions_comments = comments
        defer_obj.admissions_approved = False
        defer_obj.save()
    elif role.name == 'Dean':
        defer_obj.dean_comments = comments
        defer_obj.dean_approved = False
        defer_obj.save()
    elif role.name == 'Registrar':
        defer_obj.registrar_comments = comments
        defer_obj.registrar_approved = False
        defer_obj.save()
    elif role.name == 'DVC':
        defer_obj.dvc_comments = comments
        defer_obj.dvc_approved = False
        defer_obj.save()
    messages.warning(request,'Application for declined made')
    return redirect("manage_student_approvals")



def manage_temporary_approvals(request):
    approvals = TemporaryWithdrawalApprovalWorklow.objects.all()
    temporary_deferrement_approval_workflow_form = TemporaryDefferementApprovalWorkflowForm()
    try:
        role = HOD.objects.get(admin=request.user.id).hod_type
        context = {
            "approvals":approvals,
            "deferrement_approval_workflow_form":temporary_deferrement_approval_workflow_form,
            "role":role
        }
        
        return render(request, "admin_template/manage_temporary_approvals.html", context)
    except ObjectDoesNotExist:
        not_authorized = True
        context = {
            "approvals":approvals,
            "deferrement_approval_workflow_form":temporary_deferrement_approval_workflow_form,
            # "not_authorized": not_authorized
            # "role":role
        }
        return render(request, "admin_template/manage_temporary_approvals.html", context)

def confirm_temporary_defer(request):
    id = request.POST.get('id')
    comments = request.POST.get('comments')

    print(f'comments - [{comments}]')
    print(id)
    print(request.user)

    # try:
    role = HOD.objects.get(admin=request.user.id).hod_type
    if not role:
        messages.success(request,'Application for deferrment made')
        return JsonResponse({'error': 'You arent permitted to perfom the action'}, status=400)
    defer_obj = TemporaryWithdrawalApprovalWorklow.objects.get(id=id)
    print(defer_obj)
    if role.name == 'Admissions':
        defer_obj.admissions_comments = comments
        defer_obj.admissions_approved = True
        defer_obj.save()
    elif role.name == 'Dean':
        defer_obj.dean_comments = comments
        defer_obj.dean_approved = True
        defer_obj.save()
    elif role.name == 'Registrar':
        defer_obj.registrar_comments = comments
        defer_obj.registrar_approved = True
        defer_obj.save()
    elif role.name == 'DVC':
        defer_obj.dvc_comments = comments
        defer_obj.dvc_approved = True
        defer_obj.applicant.academic_status = 3
        print(defer_obj.applicant)
        print(defer_obj.applicant.academic_status)
        defer_obj.save()
    messages.success(request,'Application for deferrment made')
    return redirect("manage_temporary_approvals")

def deny_temporary_defer(request):
    id = request.POST.get('id')
    comments = request.POST.get('comments')

    print(f'comments - [{comments}]')
    print(id)
    print(request.user)

    # try:
    role = HOD.objects.get(admin=request.user.id).hod_type
    print(role)
    defer_obj = TemporaryWithdrawalApprovalWorklow.objects.get(id=id)
    print(defer_obj)
    if role.name == 'Admissions':
        defer_obj.admissions_comments = comments
        defer_obj.admissions_approved = False
        defer_obj.save()
    elif role.name == 'Dean':
        defer_obj.dean_comments = comments
        defer_obj.dean_approved = False
        defer_obj.save()
    elif role.name == 'Registrar':
        defer_obj.registrar_comments = comments
        defer_obj.registrar_approved = False
        defer_obj.save()
    elif role.name == 'DVC':
        defer_obj.dvc_comments = comments
        defer_obj.dvc_approved = False
        defer_obj.save()
    messages.warning(request,'Application for declined made')
    return redirect("manage_temporary_approvals")



def manage_interfaculty_transfer(request):
    approvals = InterFacultyTransferApprovalWorklow.objects.all()
    temporary_deferrement_approval_workflow_form = InterFacultyTransferWorkflowForm()
    try:
        role = HOD.objects.get(admin=request.user.id).hod_type
        context = {
            "approvals":approvals,
            "deferrement_approval_workflow_form":temporary_deferrement_approval_workflow_form,
            "role":role
        }
        
        return render(request, "admin_template/manage_student_transfer_template.html", context)
    except ObjectDoesNotExist:
        not_authorized = True
        context = {
            "approvals":approvals,
            "deferrement_approval_workflow_form":temporary_deferrement_approval_workflow_form,
            # "not_authorized": not_authorized
            # "role":role
        }
        return render(request, "admin_template/manage_student_transfer_template.html", context)


def confirm_interfaculty_transfer(request):
    id = request.POST.get('id')
    comments = request.POST.get('comments')

    print(f'comments - [{comments}]')
    print(id)
    print(request.user)

    # try:
    role = HOD.objects.get(admin=request.user.id).hod_type
    if not role:
        return JsonResponse({'error': 'You arent permitted to perfom the action'}, status=400)
    defer_obj = InterFacultyTransferApprovalWorklow.objects.get(id=id)
    
    print(defer_obj)
    if role.name == 'Admissions':
        defer_obj.admissions_comments = comments
        defer_obj.admissions_approved = True
        defer_obj.save()
    elif role.name == 'Dean':
        defer_obj.dean_comments = comments
        defer_obj.dean_approved = True
        defer_obj.save()
    elif role.name == 'Registrar':
        defer_obj.registrar_comments = comments
        defer_obj.registrar_approved = True
        defer_obj.save()
    elif role.name == 'DVC':
        defer_obj.dvc_comments = comments
        defer_obj.dvc_approved = True
        applicant_id = defer_obj.applicant.id
        new_course = defer_obj.desired_course.id
        student = Students.objects.get(id=applicant_id)
        student.course_id = new_course
        student.save()
        defer_obj.save()
    messages.success(request,'Application for deferrment made')
    return redirect("manage_temporary_approvals")

def deny_interfaculty_transfer(request):
    id = request.POST.get('id')
    comments = request.POST.get('comments')

    print(f'comments - [{comments}]')
    print(id)
    print(request.user)

    # try:
    role = HOD.objects.get(admin=request.user.id).hod_type
    print(role)
    defer_obj = InterFacultyTransferApprovalWorklow.objects.get(id=id)
    print(defer_obj)

    if role.name == 'Admissions':
        defer_obj.admissions_comments = comments
        defer_obj.admissions_approved = False
        defer_obj.save()
    elif role.name == 'Dean':
        defer_obj.dean_comments = comments
        defer_obj.dean_approved = False
        defer_obj.save()
    elif role.name == 'Registrar':
        defer_obj.registrar_comments = comments
        defer_obj.registrar_approved = False
        defer_obj.save()
    elif role.name == 'DVC':
        defer_obj.dvc_comments = comments
        defer_obj.dvc_approved = False
        defer_obj.save()
    messages.warning(request,'Application for declined made')
    return redirect("manage_temporary_approvals")