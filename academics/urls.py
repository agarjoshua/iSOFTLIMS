from django.urls import path, include

from academics.subviews import classView
from . import views
# from . import subviews.classView

urlpatterns = [
    # COURSE URLS
    path('add_class/', classView.add_class, name="add_class"),
    path('add_class_save/', classView.add_class_save, name="add_class_save"),
    path('manage_class/', classView.manage_class, name="manage_class"),
    path('edit_class/<class_id>/', classView.edit_class, name="edit_class"),
    path('edit_class_save/', classView.edit_class_save, name="edit_class_save"),
    path('delete_class/<class_id>/', classView.delete_class, name="delete_class"),

    # UTILITY URLS
    path('check_class_exist/', classView.check_class_exist, name="check_class_exist"),

]