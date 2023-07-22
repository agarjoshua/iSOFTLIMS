from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages

from core.models import CustomUser



def user_home(request):
    users = CustomUser.objects.all()
    user = request.user
    print(user)
    context = {
        "users":users,
        "user":user,
    }
    return render(request, "user_home.html", context)