from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from core.models import HOD, CustomUser, Institution, Staff
from iSOFTLIMS import settings
from iSOFTLIMS.utils.auth.password_reset import ForgotPasswordTokenGenerator
from iSOFTLIMS.utils.mail_engine import send_mail
from .utils.mail import EmailBackEnd
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib import messages

# from .EmailBackend import EmailBackEnd
from django.contrib.auth import authenticate


# Imports for password reset
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)


import sendgrid
from sendgrid.helpers.mail import Mail
from django.shortcuts import redirect, render
from django.contrib.auth.models import User


from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# Create your views here.

from django.contrib.messages.views import SuccessMessageMixin

## USER AUTH CRUD
def home(request):
    return render(request, 'index.html')

def loginPage(request):
    return render(request, 'login.html')

def applicantloginPage(request):
    return render(request, 'applicantsignup.html')

# def doLogin(request):
#     if request.method != "POST":
#         return HttpResponse("<h2>Method Not Allowed</h2>")
    

#     # user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
#     user = authenticate(request, email=request.POST.get('email'), password=request.POST.get('password'))

#     if user != None:
#         login(request, user)
#         user_type = user.user_type # type: ignore
#         #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
#         if user.account_status == 'Active': # type: ignore
#             if user_type == '1':
#                 return redirect('admin_home')
#             elif user_type == '2':
#                 specified_staff = Staff.objects.get(admin=user)
#                 staff_dept = specified_staff.associated_department # type: ignore
#                 if staff_dept.name == 'Finance': # type: ignore
#                     return redirect('finance:finance_home')
#                 if staff_dept.name == 'Admissions': # type: ignore
#                     return redirect('admissions')
#                 if staff_dept.name == 'Management': # type: ignore
#                     return redirect('admin_home')
#                 return redirect('staff_home')
#             elif user_type == '3':
#                 return redirect('student_home')
#             elif user_type == '4':
#                 specified_staff = HOD.objects.get(admin=user)
#                 hod_dept = specified_staff.associated_department # type: ignore
#                 print(hod_dept)
#                 if hod_dept!=None and hod_dept.name == 'Finance': # type: ignore
#                     return redirect('finance:finance_home')
#                 if hod_dept!=None and hod_dept.name == 'Admissions': # type: ignore
#                     return redirect('admissions')
#                 return redirect('admin_home')
#             # elif user_type == '5':
#             #     # return HttpResponse("Student Login")
#             #     return redirect('student_home')
#             elif user_type == '6':
#                 # return HttpResponse("Staff Login")
#                 return redirect('academics:teacher_home')
#             elif user_type == '8':
#                 return redirect('applicant_home')
            
#         # Increment login attempts and check if limit reached
#             user.login_attempts += 1
#             if user.login_attempts >= 3:
#                 user.account_status = 'Deactivated'
#                 user.cooldown_end_time = timezone.now() + timedelta(hours=24)

#             user.save()

#             if user.account_status == 'Deactivated':
#                 messages.error(request, "Account deactivated due to too many login attempts!")
#             else:
#                 messages.error(request, "Invalid Login!")

#             return redirect('login')
    
#         if user.account_status == 'Active':
#             messages.error(request, "Account deactivated due to too many login attempts!")
#             return redirect('login')
#         else:
#             messages.error(request, "Invalid Login!")
#             return redirect('login')
        
#     else:
#         messages.error(request, "Invalid Login Credentials!")
#         return redirect('login')
    
def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    user = authenticate(request, email=request.POST.get('email'), password=request.POST.get('password'))

    if user is not None:
        login(request, user)
        user_type = user.user_type

        if user.account_status == 'Deactivated':
            messages.error(request, "Account deactivated due to too many login attempts, click activate for admin to reset!")

        if user.account_status == 'Active':
            if user_type == '1':
                return redirect('user_home')
            elif user_type == '2':
                specified_staff = Staff.objects.get(admin=user)
                staff_dept = specified_staff.associated_department
                if staff_dept.name == 'Finance':
                    return redirect('finance:finance_home')
                if staff_dept.name == 'Admissions':
                    return redirect('admissions')
                if staff_dept.name == 'Management':
                    return redirect('admin_home')
                return redirect('staff_home')
            elif user_type == '3':
                return redirect('student_home')
            elif user_type == '4':
                specified_staff = HOD.objects.get(admin=user)
                hod_dept = specified_staff.associated_department
                print(hod_dept)
                if hod_dept is not None and hod_dept.name == 'Finance':
                    return redirect('finance:finance_home')
                if hod_dept is not None and hod_dept.name == 'Admissions':
                    return redirect('admissions')
                return redirect('admin_home')
            elif user_type == '6':
                return redirect('academics:teacher_home')
            elif user_type == '8':
                return redirect('applicant_home')

        # Increment login attempts and check if limit reached
        user.login_attempts += 1
        if user.login_attempts >= 3:
            user.account_status = 'Deactivated'
            user.cooldown_end_time = timezone.now() + timedelta(hours=24)

        user.save()

        # if user.account_status == 'Deactivated':
        #     messages.error(request, "Account deactivated due to too many login attempts!")
        # else:
        #     messages.error(request, "Invalid Login!")

        return redirect('login')
    else:
        messages.error(request, "Invalid Login Credentials!")
        return redirect('login')



def activate_account(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            if user.account_status == 'Deactivated':
                user.account_status = 'Activation Requested'
                user.save()
                messages.success(request, "If your account is deactivated and credentials are valid you'll receive an email of activation!")
                return redirect('login')
        except CustomUser.DoesNotExist:
            messages.success(request, "If your account is deactivated and credentials are valid you'll receive an email of activation!")
            return redirect('login')
    return render(request, 'activate_account.html')




def get_user_details(request):
    if request.user != None:
        return HttpResponse(f"User: {request.user.email} User Type: {request.user.user_type}")
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


