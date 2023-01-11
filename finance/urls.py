from django.urls import path, include
from . import views
from finance import views

app_name = "finance"

urlpatterns = [
    path("", views.finance, name="home"),
    path("pay", views.pay, name="pay"),
    path('check_student_exist/', views.check_student_exist, name="check_student_exist"),
]