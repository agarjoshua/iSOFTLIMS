from django.urls import path, include

from academics.subviews import classView, studentView
from iSOFTLIMS import utils
from . import views
from core.subviews import AdminViews, StudentViews, StudentAdminAffairs, ApplicantViews, UserViews
from django.contrib.auth import views as auth_views

urlpatterns = [
    



    # HOMEPAGE URL
    path("", views.loginPage, name="login"),
    path("login", views.loginPage, name="login"),
    path("register/", views.applicantloginPage, name="register"),
    path("doSignUp/", ApplicantViews.applicantsignup, name="doSignUp"),  # type: ignore
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("applicant_home/", ApplicantViews.applicant_home, name="applicant_home"),  # type: ignore
    path("user_home/", UserViews.user_home, name="user_home"),

    # USER CRUD URLS
    path("doLogin/", views.doLogin, name="doLogin"),
    path("get_user_details/", views.get_user_details, name="get_user_details"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("activate_account", views.activate_account, name="activate_account"),
    path("activate_user/<user_id>", AdminViews.activate_user, name="activate_user"),
    path(
        "deactivate_user/<user_id>", AdminViews.deactivate_user, name="deactivate_user"
    ),

    # ADMIN URLS
    path("admin_home/", AdminViews.admin_home, name="admin_home"),
    path("manage_users/", AdminViews.manage_users, name="manage_users"),

    # SCHOOL PROFILE URLS
    path("admin_profile/", AdminViews.admin_profile, name="admin_profile"),
    path("admin_profile_update/", AdminViews.admin_profile_update, name="admin_profile_update"),
    path("school_profile/", AdminViews.school_profile, name="school_profile"),
    path("admin_school_update/", AdminViews.admin_school_update, name="admin_school_update"),

    # ADMINISTRATION URLS:
    path("administration/", AdminViews.administration, name="administration"),
    path("add_campus/", AdminViews.add_campus, name="add_campus"),
    path("edit_campus/<campus_id>", AdminViews.edit_campus, name="edit_campus"),
    path("delete_campus/<campus_id>", AdminViews.delete_campus, name="delete_campus"),
    path("schools/", AdminViews.school, name="schools"),
    path("add_school/", AdminViews.add_school, name="add_school"),
    path("edit_school/<school_id>", AdminViews.edit_school, name="edit_school"),
    path("delete_school/<school_id>", AdminViews.delete_school, name="delete_school"),

    # ADMISSIONS
    path("admissions/", AdminViews.admissions, name="admissions"),
    path("admissions_approve/", AdminViews.admissions_approve, name="admissions_approve"),
    path("dvc_approve/", AdminViews.dvc_approve, name="dvc_approve"),

    # DEPARTMENT MANAGEMENT URLS
    path("manage_department/", AdminViews.manage_departments, name="manage_departments"),
    path("add_department/", AdminViews.add_department, name="add_department"),
    path("add_department_save/", AdminViews.add_department_save, name="add_department_save"),
    path("edit_department/<department_id>/", AdminViews.edit_department, name="edit_department"),
    path("edit_department_save/", AdminViews.edit_department_save, name="edit_department_save"),
    path("delete_department/<department_id>/", AdminViews.delete_department, name="delete_department"),
    path("manage_staff_type/", AdminViews.manage_staff_type, name="manage_staff_type"),
    path("create_staff_type/", AdminViews.create_staff_type, name="create_staff_type"),

    # HOD URLS
    path("manage_hod/", AdminViews.manage_hods, name="manage_hod"),
    path("add_hod/", AdminViews.add_hod, name="add_hod"),
    path("add_hod_save/", AdminViews.add_hod_save, name="add_hod_save"),
    path("edit_hod/<hod_id>/", AdminViews.edit_hod, name="edit_hod"),
    path("edit_hod_save/", AdminViews.edit_hod_save, name="edit_hod_save"),
    path("delete_hod/<hod_id>/", AdminViews.delete_hod, name="delete_hod"),

    # MANAGE COURSE
    path("manage_courses/", AdminViews.manage_courses, name="manage_courses"),
    path("add_course/", AdminViews.add_course, name="add_course"),
    path("add_course_save/", AdminViews.add_course_save, name="add_course_save"),
    path("check_if_course_exists/", AdminViews.check_if_course_exists, name="check_if_course_exists"),
    path("edit_course/<course_id>", AdminViews.edit_course, name="edit_course"),
    path("delete_course/<course_id>", AdminViews.delete_course, name="delete_course"),

    # STAFF URLS
    path("add_staff/", AdminViews.add_staff, name="add_staff"),
    path("add_staff_save/", AdminViews.add_staff_save, name="add_staff_save"),
    path("manage_staff/", AdminViews.manage_staff, name="manage_staff"),
    path("edit_staff/<staff_id>/", AdminViews.edit_staff, name="edit_staff"),
    path("edit_teacher/<teacher_id>/", AdminViews.edit_teacher, name="edit_teacher"),
    path("edit_staff_save/", AdminViews.edit_staff_save, name="edit_staff_save"),
    path("edit_teacher_save/", AdminViews.edit_teacher_save, name="edit_teacher_save"),
    path("delete_staff/<staff_id>/", AdminViews.delete_staff, name="delete_staff"),
    path("delete_teacher/<teacher_id>/", AdminViews.delete_teacher, name="delete_teacher"),

    # STUDENT URLS
    path("student_home", StudentViews.student_home, name="student_home"),
    path("student_profile/", StudentViews.student_profile, name="student_profile"),
    path("student_sessions/", StudentViews.enroll_session, name="enroll_session"),
    path("enroll_session_save/<enrollment_id>", StudentViews.enroll_session_save, name="enroll_session_save"),
    path("student_classes/", StudentViews.enroll_classes, name="enroll_classes"),
    path("enroll_class_save/", StudentViews.enroll_class_save, name="enroll_class_save"),
    path("student_apply_leave/", StudentViews.student_apply_leave, name="student_apply_leave"),
    path("student_apply_leave_save/", StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    path("student_feedback/", StudentViews.student_feedback, name="student_feedback"),
    path("student_feedback_save/", StudentViews.student_feedback_save, name="student_feedback_save"),
    path("student_profile/", StudentViews.student_profile, name="student_profile"),
    path("student_profile_update/", StudentViews.student_profile_update, name="student_profile_update"),
    path("student_view_result/", StudentViews.student_view_result, name="student_view_result"),

    path("student_housing/", StudentViews.student_housing, name="student_housing"),
    path("book_housing/<house_id>", StudentViews.book_housing, name="book_housing"),
    



    path("add_student/", AdminViews.add_student, name="add_student"),
    path("add_student_save/", AdminViews.add_student_save, name="add_student_save"),
    path("edit_student/<student_id>", AdminViews.edit_student, name="edit_student"),
    path("edit_student_save/", AdminViews.edit_student_save, name="edit_student_save"),
    path("manage_students/", AdminViews.manage_students, name="manage_students"),
    path("delete_student/<student_id>/", AdminViews.delete_student, name="delete_student"),
    path("student_session_management/", StudentViews.students_sessions_management, name="students_sessions_management"),
    path("defer_student/", StudentViews.defer_student, name="defer_student"),
    path("withdraw_student/", StudentViews.withdraw_student, name="withdraw_student"),
    path("student_affairs/", StudentAdminAffairs.student_affairs_home, name="student_affairs"),
    path("manage_student_approvals/", StudentAdminAffairs.manage_student_approvals, name="manage_student_approvals"),
    path("confirm_defer_student/", StudentAdminAffairs.confirm_defer_student, name="confirm_defer_student"),
    path("deny_defer_student/", StudentAdminAffairs.deny_defer_student, name="deny_defer_student"),
    path("manage_temporary_approvals/", StudentAdminAffairs.manage_temporary_approvals, name="manage_temporary_approvals"),
    path("confirm_temporary_defer/", StudentAdminAffairs.confirm_temporary_defer, name="confirm_temporary_defer"),
    path("deny_temporary_defer/", StudentAdminAffairs.deny_temporary_defer, name="deny_temporary_defer"),
    path("manage_interfaculty_transfer/", StudentAdminAffairs.manage_interfaculty_transfer, name="manage_interfaculty_transfer"),
    path("confirm_interfaculty_transfer/", StudentAdminAffairs.confirm_interfaculty_transfer, name="confirm_interfaculty_transfer"),
    path("deny_interfaculty_transfer/", StudentAdminAffairs.deny_interfaculty_transfer, name="deny_interfaculty_transfer"),
    path("manage_guardians/", AdminViews.manage_guardians, name="manage_guardians"),
    path("add_guardians/", AdminViews.add_guardian, name="add_guardian"),
    path("add_guardian_save/", AdminViews.add_guardian_save, name="add_guardian_save"),
    path("edit_guardian/<guardian_id>/", AdminViews.edit_guardian, name="edit_guardian"),
    path("edit_guardian_save/", AdminViews.edit_guardian_save, name="edit_guardian_save"),
    path("delete_guardian/<guardian_id>/", AdminViews.delete_student, name="delete_guardian"),

    path("apply_interschool_transfer/", StudentAdminAffairs.apply_interschool_transfer, name="apply_interschool_transfer"),
    # path("apply_interfaculty_transfer_save/", StudentAdminAffairs.apply_interfaculty_transfer_save, name="apply_interfaculty_transfer_save"),
    path("apply_interfaculty_transfer/", StudentAdminAffairs.apply_interfaculty_transfer, name="apply_interfaculty_transfer"),


    # PROCESSES
    path("processes", AdminViews.processes, name="processes"),


    # HOUSES
    path("manage_houses", AdminViews.manage_houses, name="manage_houses"),
    path("add_house", AdminViews.add_house, name="add_house"),
    path("add_house_save", AdminViews.add_house_save, name="add_house_save"),
    path("edit_house/<house_id>", AdminViews.edit_house, name="edit_house"),
    path("delete_house/<house_id>", AdminViews.delete_house, name="delete_house"),

    path("manage_booking", AdminViews.manage_booking, name="manage_booking"),
    path("confirm_booking/<booking_id>", AdminViews.confirm_booking, name="confirm_booking"),

    # SERVICES
    path("manage_services", AdminViews.manage_services, name="manage_services"),
    path("add_service", AdminViews.add_service, name="add_service"),
    path("add_service_save", AdminViews.add_service_save, name="add_service_save"),
    path("edit_service/<service_id>", AdminViews.edit_service, name="edit_service"),
    path("delete_service/<service_id>", AdminViews.delete_service, name="delete_service"),

    # EC Activities
    path("manage_activities", AdminViews.manage_activities, name="manage_activities"),
    path("add_activities", AdminViews.add_activities, name="add_activities"),
    path("add_activities_save", AdminViews.add_activities_save, name="add_activities_save"),
    path("edit_activity/<service_id>", AdminViews.edit_activities, name="edit_activity"),
    path("delete_activity/<service_id>", AdminViews.delete_activities, name="delete_activity"),

    # JOBS & POSITIONS
    path("manage_jobs", AdminViews.manage_jobs, name="manage_jobs"),
    path("add_job", AdminViews.add_job, name="add_job"),
    path("add_job_save", AdminViews.add_job_save, name="add_job_save"),
    path("edit_job/<job_id>", AdminViews.edit_job, name="edit_job"),
    path("delete_job/<job_id>", AdminViews.delete_job, name="delete_job"),

    # USER RESPONSIBILITY 
    path("manage_responsibilities", AdminViews.manage_responsibilities, name="manage_responsibilities"),
    path("add_responsibility", AdminViews.add_responsibility, name="add_responsibility"),
    path("add_responsibility_save", AdminViews.add_responsibility_save, name="add_responsibility_save"),
    path("edit_responsibility/<responsibility_id>", AdminViews.edit_responsibility, name="edit_responsibility"),
    path("delete_responsibility/<responsibility_id>", AdminViews.delete_responsibility, name="delete_responsibility"),

    # DISCIPLINARY MANAGEMENT
    path("manage_disciplinary_issues", AdminViews.manage_disciplinary_issues, name="manage_disciplinary_issues"),
    path("add_disciplinary_issue", AdminViews.add_disciplinary_issue, name="add_disciplinary_issue"),
    path("add_disciplinary_issue_save", AdminViews.add_disciplinary_issue_save, name="add_disciplinary_issue_save"),
    path("edit_disciplinary_issue/<disciplinary_id>", AdminViews.edit_disciplinary_issue, name="edit_disciplinary_issue"),
    path("delete_disciplinary_issue/<disciplinary_id>", AdminViews.delete_disciplinary_issue, name="delete_disciplinary_issue"),

    # PAYMENT METHODS
    path("manage_payment_methods", AdminViews.manage_payment_methods, name="manage_payment_methods"),
    path("add_payment_method", AdminViews.add_payment_method, name="add_payment_method"),
    path("add_payment_method_save", AdminViews.add_payment_method_save, name="add_payment_method_save"),
    path("edit_payment_method/<payment_method_id>", AdminViews.edit_payment_method, name="edit_payment_method"),
    path("delete_payment_method/<payment_method_id>", AdminViews.delete_payment_method, name="delete_payment_method"),
    # banks
    path("manage_banks", AdminViews.manage_banks, name="manage_banks"),
    path("add_bank", AdminViews.add_bank, name="add_bank"),
    path("add_bank_save", AdminViews.add_bank_save, name="add_bank_save"),
    path("edit_bank/<bank_id>", AdminViews.edit_bank, name="edit_bank"),
    path("delete_bank/<bank_id>", AdminViews.delete_bank, name="delete_bank"),

    # FEE ITEMS
    path("manage_fee_items", AdminViews.manage_fee_items, name="manage_fee_items"),
    path("add_fee_item", AdminViews.add_fee_item, name="add_fee_item"),
    path("add_fee_item_save", AdminViews.add_fee_item_save, name="add_fee_item_save"),
    path("edit_fee_item/<fee_item_id>", AdminViews.edit_fee_item, name="edit_fee_item"),
    path("delete_fee_item/<fee_item_id>", AdminViews.delete_fee_item, name="delete_fee_item"),

    # BILLING TEMPLATES
    path("manage_billing_templates", AdminViews.manage_billing_templates, name="manage_billing_templates"),
    path("add_billing_template", AdminViews.add_billing_template, name="add_billing_template"),
    path("add_billing_template_save", AdminViews.add_billing_template_save, name="add_billing_template_save"),
    path("edit_billing_template/<billing_template_id>", AdminViews.edit_billing_template, name="edit_billing_template"),
    path("delete_billing_template/<billing_template_id>", AdminViews.delete_billing_template, name="delete_billing_template"),

    

    # REPORTS
    path("reports/", AdminViews.reports, name="reports"),
    
    
    # UTILITIES
    path("check_email_exist/", AdminViews.check_email_exist, name="check_email_exist"),
    path("check_username_exist/", AdminViews.check_username_exist, name="check_username_exist"),
    path("check_department_exist/", AdminViews.check_department_exist, name="check_department_exist")

]


# INACTIVE URL ENDPOINTS
# path('reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # # path('reset/', views.send_reset_email, name='password_reset'),
    # path('reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/confirm/<uidb64>/<token>/', views.ResetPasswordView.as_view(), name='password_reset_confirm'),
    # path('reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('password/', include('password_reset.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    #     path('manage_users/', AdminViews.edit_users, name="manage_users"),
    # path('admin_view_attendance/', AdminViews.admin_view_attendance, name="admin_view_attendance"),
    # path('admin_get_attendance_dates/', AdminViews.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    # path('admin_get_attendance_student/', AdminViews.admin_get_attendance_student, name="admin_get_attendance_student"),
    # path('staff_feedback_message/', AdminViews.staff_feedback_message, name="staff_feedback_message"),
    # path('staff_feedback_message_reply/', AdminViews.staff_feedback_message_reply, name="staff_feedback_message_reply"),
    # path('staff_leave_view/', AdminViews.staff_leave_view, name="staff_leave_view"),
    # path('staff_leave_approve/<leave_id>/', AdminViews.staff_leave_approve, name="staff_leave_approve"),
    # path('staff_leave_reject/<leave_id>/', AdminViews.staff_leave_reject, name="staff_leave_reject"),
    # path('student_classes/', StudentViews.enroll_classes, name="enroll_classes"),
    # path('edit_student/<student_id>', StudentViews.edit_student, name="edit_student"),
    # path('edit_student_save/', StudentViews.edit_student_save, name="edit_student_save"),
    # path('student_view_attendance/', StudentViews.student_view_attendance, name="student_view_attendance"),
    # path('student_view_attendance_post/', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
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
    # path('generate_pdf/', AdminViews.generate_table_pdf, name="generate_pdf"),
    # path('check_cluster_class_exist/', classView.check_cluster_class_exist, name="check_cluster_class_exist")