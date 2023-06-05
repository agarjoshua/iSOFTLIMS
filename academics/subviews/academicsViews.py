from django.shortcuts import render

from academics.models import Session
# from .models import Fee, Transaction


def academics_home(request):
    session_years = Session.objects.all()
    context = {"session_years": session_years[:3]}
    
    return render(request, "academics_home.html", context)
 # type: ignore