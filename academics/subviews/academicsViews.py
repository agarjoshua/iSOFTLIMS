from django.shortcuts import redirect, render
from academics.forms.communicationForms import AcademicCommunicationForm

from academics.models import AcademicCommunications, Session
# from .models import Fee, Transaction
from django.contrib import messages
from core.subviews.utilities.accesscontrolutilities import allow_user

# USER NUMBER REFERENCE
# 1 = ADMIN
# 2 = STAFF
# 3 = STUDENTS
# 4 = HOD
# 5 = GUARDIAN
# 6 = TEACHER
@allow_user('1','4','6') 
def academics_home(request):
    session_years = Session.objects.all()
    communicationsform = AcademicCommunicationForm()
    communication_list = AcademicCommunications.objects.all()
    sessions_number = session_years.count()
    context = {
        "session_years": session_years[:3],
        "communicationsform": communicationsform,
        "communication_list": communication_list,
        "sessions_number":sessions_number
        }
    
    return render(request, "academics_home.html", context)

@allow_user('1','4','6') 
def academics_comm_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("academics:academics_home")
    else:
        try:
            form = AcademicCommunicationForm(request.POST)
            form.save()
            messages.success(request, 'Communication sent')
            return redirect('academics:academics_home')
        except Exception as e:
            messages.error(request, f'Could not be added because - {e}')
            return redirect('academics:academics_home')