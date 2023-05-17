from django.urls import path, include

from academics.subviews import classView, studentView
from . import views
from core.subviews import AdminViews, StudentViews,StudentAdminAffairs, ApplicantViews

urlpatterns = [

    #HOMEPAGE URL
    path('', views.loginPage, name="login"),
    path("login", views.loginPage, name="login"),
    path("register/", views.applicantloginPage, name="register"),
    path("doSignUp/", ApplicantViews.applicantsignup, name="doSignUp"), # type: ignore
    path('applicant_home/', ApplicantViews.applicant_home, name="applicant_home"), # type: ignore
    

    #USER CRUD URLS
    # path('accounts/', include('django.contrib.auth.urls')),
    path("doLogin/", views.doLogin, name="doLogin"),
    path("get_user_details/", views.get_user_details, name="get_user_details"),
    path("logout_user/", views.logout_user, name="logout_user"),


    # ADMIN URLS
    path('doLogin/', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin_home/', AdminViews.admin_home, name="admin_home"),
    # path('admin_view_attendance/', AdminViews.admin_view_attendance, name="admin_view_attendance"),
    # path('admin_get_attendance_dates/', AdminViews.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    # path('admin_get_attendance_student/', AdminViews.admin_get_attendance_student, name="admin_get_attendance_student"),

    # SCHOOL PROFILE URLS
    path('admin_profile/', AdminViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', AdminViews.admin_profile_update, name="admin_profile_update"),
    path('school_profile/', AdminViews.school_profile, name="school_profile"),
    path('admin_school_update/', AdminViews.admin_school_update, name="admin_school_update"),

    # ADMISSIONS
    path('admissions/', AdminViews.admissions, name="admissions"),
    path('admissions_approve/', AdminViews.admissions_approve, name="admissions_approve"),
    path('dvc_approve/', AdminViews.dvc_approve, name="dvc_approve"),
    
    

    # DEPARTMENT MANAGEMENT URLS      
    path('manage_department/', AdminViews.manage_departments, name="manage_departments"),
    path('add_department/', AdminViews.add_department, name="add_department"),
    path('add_department_save/', AdminViews.add_department_save, name="add_department_save"),
    path('edit_department/<department_id>/', AdminViews.edit_department, name="edit_department"),
    path('edit_department_save/', AdminViews.edit_department_save, name="edit_department_save"),
    path('delete_department/<department_id>/', AdminViews.delete_department, name="delete_department"),

    path('manage_staff_type/', AdminViews.manage_staff_type, name="manage_staff_type"),
    # path('add_stafftype/', AdminViews.manage_staff_type, name="add_stafftype"),
    path("create_staff_type/", AdminViews.create_staff_type, name="create_staff_type"),
    

    # HOD URLS      
    path('manage_hod/', AdminViews.manage_hods, name="manage_hod"),
    path('add_hod/', AdminViews.add_hod, name="add_hod"),
    path('add_hod_save/', AdminViews.add_hod_save, name="add_hod_save"),
    path('edit_hod/<hod_id>/', AdminViews.edit_hod, name="edit_hod"),
    path('edit_hod_save/', AdminViews.edit_hod_save, name="edit_hod_save"),
    path('delete_hod/<hod_id>/', AdminViews.delete_hod, name="delete_hod"),

    # STAFF URLS
    path('add_staff/', AdminViews.add_staff, name="add_staff"),
    path('add_staff_save/', AdminViews.add_staff_save, name="add_staff_save"),
    path('manage_staff/', AdminViews.manage_staff, name="manage_staff"),
    path('edit_staff/<staff_id>/', AdminViews.edit_staff, name="edit_staff"),
    path('edit_staff_save/', AdminViews.edit_staff_save, name="edit_staff_save"),
    path('delete_staff/<staff_id>/', AdminViews.delete_staff, name="delete_staff"),
    # path('staff_feedback_message/', AdminViews.staff_feedback_message, name="staff_feedback_message"),
    # path('staff_feedback_message_reply/', AdminViews.staff_feedback_message_reply, name="staff_feedback_message_reply"),
    # path('staff_leave_view/', AdminViews.staff_leave_view, name="staff_leave_view"),
    # path('staff_leave_approve/<leave_id>/', AdminViews.staff_leave_approve, name="staff_leave_approve"),
    # path('staff_leave_reject/<leave_id>/', AdminViews.staff_leave_reject, name="staff_leave_reject"),
    

    # STUDENT URLS
    path('student_home', StudentViews.student_home, name="student_home"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_sessions/', StudentViews.enroll_session, name="enroll_session"),
    path('enroll_session_save/<enrollment_id>', StudentViews.enroll_session_save, name="enroll_session_save"),
    path('student_classes/', StudentViews.enroll_classes, name="enroll_classes"),
    path('enroll_class_save/', StudentViews.enroll_class_save, name="enroll_class_save"),
    # path('student_classes/', StudentViews.enroll_classes, name="enroll_classes"),

    # path('edit_student/<student_id>', StudentViews.edit_student, name="edit_student"),
    # path('edit_student_save/', StudentViews.edit_student_save, name="edit_student_save"),
    # path('student_view_attendance/', StudentViews.student_view_attendance, name="student_view_attendance"),
    # path('student_view_attendance_post/', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_apply_leave/', StudentViews.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save/', StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback/', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save/', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"),
    path('student_view_result/', StudentViews.student_view_result, name="student_view_result"),
    

    path('add_student/', AdminViews.add_student, name="add_student"),
    path('add_student_save/', AdminViews.add_student_save, name="add_student_save"),
    path('edit_student/<student_id>', AdminViews.edit_student, name="edit_student"),
    path('edit_student_save/', AdminViews.edit_student_save, name="edit_student_save"),
    path('manage_students/', AdminViews.manage_students, name="manage_students"),
    path('delete_student/<student_id>/', AdminViews.delete_student, name="delete_student"),

    path('student_session_management/',StudentViews.students_sessions_management,name="students_sessions_management"),
    path('defer_student/',StudentViews.defer_student,name="defer_student"),
    path("withdraw_student/", StudentViews.withdraw_student, name="withdraw_student"),

    path("student_affairs/", StudentAdminAffairs.student_affairs_home, name="student_affairs"),
    path("manage_student_approvals/", StudentAdminAffairs.manage_student_approvals, name="manage_student_approvals"),
    path('confirm_defer_student/', StudentAdminAffairs.confirm_defer_student, name='confirm_defer_student'),
    
    
    # path('student_feedback_message/', AdminViews.student_feedback_message, name="student_feedback_message"),
    # path('student_feedback_message_reply/', AdminViews.student_feedback_message_reply, name="student_feedback_message_reply"),
    # path('student_leave_view/', AdminViews.student_leave_view, name="student_leave_view"),
    # path('student_leave_approve/<leave_id>/', AdminViews.student_leave_approve, name="student_leave_approve"),
    # path('student_leave_reject/<leave_id>/', AdminViews.student_leave_reject, name="student_leave_reject"),

    # SUBJECT MANAGEMENT URLS
    # path('add_subject/', AdminViews.add_subject, name="add_subject"),
    # path('add_subject_save/', AdminViews.add_subject_save, name="add_subject_save"),
    # path('manage_subject/', AdminViews.manage_subject, name="manage_subject"),
    # path('edit_subject/<subject_id>/', AdminViews.edit_subject, name="edit_subject"),
    # path('edit_subject_save/', AdminViews.edit_subject_save, name="edit_subject_save"),
    # path('delete_subject/<subject_id>/', AdminViews.delete_subject, name="delete_subject"),


    # GUARDIAN URLS      
    path('manage_guardians/', AdminViews.manage_guardians, name="manage_guardians"),
    path('add_guardians/', AdminViews.add_guardian, name="add_guardian"),
    path('add_guardian_save/', AdminViews.add_guardian_save, name="add_guardian_save"),
    path('edit_guardian/<guardian_id>/', AdminViews.edit_guardian, name="edit_guardian"),
    path('edit_guardian_save/', AdminViews.edit_guardian_save, name="edit_guardian_save"),
    path('delete_guardian/<guardian_id>/', AdminViews.delete_student, name="delete_guardian"),


    # SESSION URLS
    path('manage_session/', AdminViews.manage_session, name="manage_session"),
    path('add_session/', AdminViews.add_session, name="add_session"),
    path('add_session_save/', AdminViews.add_session_save, name="add_session_save"),
    path('edit_session/<session_id>', AdminViews.edit_session, name="edit_session"),
    path('edit_session_save/', AdminViews.edit_session_save, name="edit_session_save"),
    path('delete_session/<session_id>/', AdminViews.delete_session, name="delete_session"),

    # COURSES URLS
    path('manage_courses/', AdminViews.manage_courses, name="manage_courses"),
    path('add_course/', AdminViews.add_course, name="add_course"),
    path('add_course_save/',AdminViews.add_course_save, name='add_course_save'),
    path('check_if_course_exists/',AdminViews.check_if_course_exists, name='check_if_course_exists'),
    path('edit_course/<course_id>',AdminViews.edit_course, name='edit_course'),
    path('delete_course/<course_id>',AdminViews.delete_course, name='delete_course'),

    # UTILITY URLS
    path('check_email_exist/', AdminViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', AdminViews.check_username_exist, name="check_username_exist"),
    # path('check_cluster_class_exist/', classView.check_cluster_class_exist, name="check_cluster_class_exist")
]
