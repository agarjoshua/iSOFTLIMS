from django.shortcuts import render, redirect

from core.models import DeferrmentApprovalWorklow


def student_affairs_home(request):

    context = {

    }
    return render(request, "admin_template/manage_student_admin_affairs.html", context)


def manage_student_approvals(request):
    approvals = DeferrmentApprovalWorklow.objects.all()
    context = {
        "approvals":approvals
    }
    return render(request, "admin_template/manage_student_approvals.html", context)