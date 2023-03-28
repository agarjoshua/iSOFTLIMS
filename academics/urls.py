from django.urls import path, include

from academics.subviews import classView
from . import views
# from . import subviews.classView

urlpatterns = [
    # Grade Year URLS
    path('add_grade/', classView.add_grade, name="add_grade"),
    path('add_class_grade/', classView.add_grade_save, name="add_grade_save"),
    path('manage_grade/', classView.manage_grade, name="manage_grade"),
    path('edit_grade/<grade_id>/', classView.edit_grade, name="edit_grade"),
    path('delete_grade/<grade_id>/', classView.delete_grade, name="delete_grade"),

    # COURSE URLS
    path('add_class/', classView.add_class, name="add_class"),
    path('add_class_save/', classView.add_class_save, name="add_class_save"),
    path('manage_class/', classView.manage_class, name="manage_class"),
    path('edit_class/<class_id>/', classView.edit_class, name="edit_class"),
    # path('edit_class_save/', classView.edit_class_save, name="edit_class_save"),
    path('delete_class/<class_id>/', classView.delete_class, name="delete_class"),

    # GRADE URLS
    path('add_grade/', classView.add_grade, name="add_grade"),
    path('add_grade_save/', classView.add_grade_save, name="add_grade_save"),
    path('manage_grade/', classView.manage_grade, name="manage_grade"),
    path('edit_grade/<grade_id>/', classView.edit_grade, name="edit_grade"),
    path('delete_grade/<grade_id>/', classView.delete_grade, name="delete_grade"),

    # UTILITY URLS
    path('check_class_exist/', classView.check_class_exist, name="check_class_exist"),

]