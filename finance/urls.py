from django.urls import path, include
from . import views
from finance import views

app_name = "finance"

urlpatterns = [
    path("finance", views.finance_home, name="finance_home"),
    path('approve_applications/', views.approve_applications, name="approve_applications"),
    path('approve/', views.approve, name="approve"),
    path('check_student_exist/', views.check_student_exist, name="check_student_exist"),
]