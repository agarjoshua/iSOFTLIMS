from django.shortcuts import render
# from .models import Fee, Transaction


def academics_home(request):
    

    context = {
    }
    return render(request, "academics/academics_home.html", context)
 # type: ignore