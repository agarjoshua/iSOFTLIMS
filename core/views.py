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


## USER AUTH CRUD
def home(request):
    return render(request, 'index.html')

def loginPage(request):
    return render(request, 'login.html')

def applicantloginPage(request):
    return render(request, 'applicantsignup.html')

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    

    # user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
    user = authenticate(request, email=request.POST.get('email'), password=request.POST.get('password'))

    if user != None:
        login(request, user)
        user_type = user.user_type
        #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
        if user_type == '1':
            return redirect('admin_home')
        elif user_type == '2':
            specified_staff = Staff.objects.get(admin=user)
            staff_dept = specified_staff.associated_department # type: ignore
            if staff_dept.name == 'Finance': # type: ignore
                return redirect('finance:finance_home')
            if staff_dept.name == 'Admissions': # type: ignore
                return redirect('admissions')
            if staff_dept.name == 'Management': # type: ignore
                return redirect('admin_home')
            return redirect('staff_home')
        elif user_type == '3':
            return redirect('student_home')
        elif user_type == '4':
            specified_staff = HOD.objects.get(admin=user)
            hod_dept = specified_staff.associated_department # type: ignore
            print(hod_dept)
            if hod_dept!=None and hod_dept.name == 'Finance': # type: ignore
                return redirect('finance:finance_home')
            if hod_dept!=None and hod_dept.name == 'Admissions': # type: ignore
                return redirect('admissions')
            return redirect('admin_home')
        # elif user_type == '5':
        #     # return HttpResponse("Student Login")
        #     return redirect('student_home')
        elif user_type == '6':
            # return HttpResponse("Staff Login")
            return redirect('academics:teacher_home')
        elif user_type == '8':
            return redirect('applicant_home')
            # return redirect('student_home')
        else:
            messages.error(request, "Invalid Login!")
            return redirect('login')
    else:
        messages.error(request, "Invalid Login Credentials!")
        #return HttpResponseRedirect("/")
        return redirect('login')

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'password_reset/email.html'
    success_url = '/reset/done/'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset/reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = '/reset/complete/'
    template_name = 'utility_templates/password_reset_confirm.html'

#     token_generator = default_token_generator
#     form_class = SetPasswordForm

#     print(form_class)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         form = context['form']
#         print(form)
#         context['form'] = form
#         return context

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset/reset_complete.html'


def send_reset_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # Handle user not found error
            return render(request, 'reset_email.html', {'error': 'User not found'})
        reset_token_generator_object = ForgotPasswordTokenGenerator()
        password_reset_token = reset_token_generator_object.make_token(user)
        reset_link = f'{_get_base_url(request)}/reset/confirm/{user.id}/{password_reset_token}'

        recepient=email
        subject='Password Reset'
        message=f'Click the link to reset your password:{reset_link}'

        try:
            send_mail(recepient,subject,message)
            print('hello')
        except Exception as e:
            return e

        # Redirect the user after sending the email
        return redirect('password_reset_done')

    return render(request, 'utility_templates/reset_email.html')

def _get_base_url(request):
    if settings.DEBUG:
        # Running locally
        return request.build_absolute_uri('/')[:-1]
    else:
        # Hosted environment
        return 'https://isoft.azurewebsites.net/'
    

def custom_password_reset_confirm(request, uidb64, token):
    # Retrieve user and perform token validation (code omitted for brevity)

    # Create the password reset confirmation form
    form = SetPasswordForm(user=user)

    # Render the template with the form and other necessary context variables
    context = {
        'form': form,
    }
    return render(request, 'password_reset_confirm.html', context)

def get_user_details(request):
    if request.user != None:
        return HttpResponse(f"User: {request.user.email} User Type: {request.user.user_type}")
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


