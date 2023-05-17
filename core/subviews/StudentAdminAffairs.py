from django.shortcuts import render, redirect
from core.forms.approvalforms import AdminDefferementApprovalWorkflowForm
from django.contrib import messages
from core.models import HOD, DeferrmentApprovalWorklow
from core.subviews.utilities.StudentViewUtilities import check_hod_type
from django.core.exceptions import ObjectDoesNotExist

def student_affairs_home(request):

    context = {

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
        defer_obj.save()
    messages.success(request,'Application for deferrment made')
    return redirect("manage_student_approvals")

    # except Exception as e:
    #     messages.error(request,f'{e}')
    #     return redirect("manage_student_approvals")