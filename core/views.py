from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from core.models import HOD, CustomUser, Institution, Staff
from .utils.mail import EmailBackEnd
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib import messages

# from .EmailBackend import EmailBackEnd


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
    user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
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



def get_user_details(request):
    if request.user != None:
        return HttpResponse(f"User: {request.user.email} User Type: {request.user.user_type}")
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


