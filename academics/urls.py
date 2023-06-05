from django.urls import path, include

from academics.subviews import TeacherViews, academicsViews, classView, sessionRegistrationView, examinationViews, sessionViews
from . import views
# from . import subviews.classView

app_name = 'academics'

urlpatterns = [

    path('', academicsViews.academics_home, name="academics_home"),
    
    path('teacher_home/', TeacherViews.teacher_home, name="teacher_home"), 

    # SESSION URLS
    path('manage_session/', sessionViews.manage_session, name="manage_session"),
    path('add_session/', sessionViews.add_session, name="add_session"),
    path('add_session_save/', sessionViews.add_session_save, name="add_session_save"),
    path('edit_session/<session_id>', sessionViews.edit_session, name="edit_session"),
    path('edit_session_save/', sessionViews.edit_session_save, name="edit_session_save"),
    path('delete_session/<session_id>/', sessionViews.delete_session, name="delete_session"),

    
    # MANAGE SESSION REGISTATION URLS
    path('manage_session_registation/', sessionRegistrationView.manage_session_registation, name="manage_session_registation"), 
    path('enroll_student/',sessionRegistrationView.enroll_student, name='enroll_student'),
    path('mass_edit_enrolled',sessionRegistrationView.mass_edit_enrolled, name='mass_edit_enrolled'),
    path('confirm_enrollment/<enrolled_id>/', sessionRegistrationView.confirm_enrollment, name='confirm_enrollment'),
    path('revoke_enrollment/<enrolled_id>/', sessionRegistrationView.revoke_enrollment, name="revoke_enrollment"),

    # Grade Year URLS
    path('add_grade/', classView.add_grade, name="add_grade"),
    path('add_class_grade/', classView.add_grade_save, name="add_grade_save"),
    path('manage_grade/', classView.manage_grade, name="manage_grade"),
    path('edit_grade/<grade_id>/', classView.edit_grade, name="edit_grade"),
    path('delete_grade/<grade_id>/', classView.delete_grade, name="delete_grade"),

    # CLASS URLS
    path('add_class/', classView.add_class, name="add_class"),
    # path('add_class_save/', classView.add_class_save, name="add_class_save"),
    path('manage_class/', classView.manage_class, name="manage_class"),

    #class clusters
    # path('manage_clusters/', classView.clusterclass_detail, name="manage_clusters"),
    path('manage_clusters/', classView.clusterclass_list, name='clusterclass_list'),
    path('<int:pk>/', classView.clusterclass_detail, name='clusterclass_detail'),
    path('new/', classView.clusterclass_create, name='clusterclass_create'),
    path('edit_clusterclass/<int:clusterclass_id>', classView.clusterclass_edit, name='clusterclass_edit'),

    path('edit_class/<class_id>/', classView.edit_class, name="edit_class"),
    # path('edit_class_save/', classView.edit_class_save, name="edit_class_save"),
    path('delete_class/<class_id>/', classView.delete_class, name="delete_class"),

    # GRADE URLS
    path('add_grade/', classView.add_grade, name="add_grade"),
    path('add_grade_save/', classView.add_grade_save, name="add_grade_save"),
    path('manage_grade/', classView.manage_grade, name="manage_grade"),
    path('edit_grade/<grade_id>/', classView.edit_grade, name="edit_grade"),
    path('delete_grade/<grade_id>/', classView.delete_grade, name="delete_grade"),

    # MANAGE EXAMINATIONS
    path('manage_exams/', examinationViews.manage_examinations, name="manage_exams"),
    path('add_exam_type/', examinationViews.add_exam_type, name="add_exam_type"),
    path('add_grade_exam/', examinationViews.add_grade, name="add_grade_exam"),
    path('add_new_grade_exam/', examinationViews.add_new_grade, name="add_new_grade_exam"),
    path('mass_edit_student_exam', examinationViews.mass_edit_student_exam, name="mass_edit_student_exam"),
    

    #student management
    path('register_for_exam/', examinationViews.register_for_exam, name="register_for_exam"),

    # UTILITY URLS
    path('check_class_exist/', classView.check_class_exist, name="check_class_exist"),
    path('check_cluster_class_exist/', classView.check_cluster_class_exist, name="check_cluster_class_exist")

]