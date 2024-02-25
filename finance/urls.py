from django.urls import path, include
from . import views
from finance import views
from .subviews import MainViews

app_name = "finance"


urlpatterns = [
    # path("finance", views.finance_home, name="finance_home"),
    path("", views.finance_home, name="finance_home"),
    path("add_transaction", views.add_transaction, name="add_transaction"),
    path("transaction_create", views.transaction_create, name='transaction_create'),
    path('approve_applications/', views.approve_applications, name="approve_applications"),
    path('approve/', views.approve, name="approve"),
    path('check_student_exist/', views.check_student_exist, name="check_student_exist"),

    # PAYMENT METHODS
    path("manage_payment_methods", MainViews.manage_payment_methods, name="manage_payment_methods"),
    path("add_payment_method", MainViews.add_payment_method, name="add_payment_method"),
    path("add_payment_method_save", MainViews.add_payment_method_save, name="add_payment_method_save"),
    path("edit_payment_method/<payment_method_id>", MainViews.edit_payment_method, name="edit_payment_method"),
    path("delete_payment_method/<payment_method_id>", MainViews.delete_payment_method, name="delete_payment_method"),
    # banks
    path("manage_banks", MainViews.manage_banks, name="manage_banks"),
    path("add_bank", MainViews.add_bank, name="add_bank"),
    path("add_bank_save", MainViews.add_bank_save, name="add_bank_save"),
    path("edit_bank/<bank_id>", MainViews.edit_bank, name="edit_bank"),
    path("delete_bank/<bank_id>", MainViews.delete_bank, name="delete_bank"),

    # billing ITEMS
    path("manage billing", MainViews.manage_billing_items, name="manage_billing_items"),
    path("add_billing_item", MainViews.add_billing_item, name="add_billing_item"),
    path("add_billing_item_save", MainViews.add_billing_item_save, name="add_billing_item_save"),
    path("edit_billing_item/<billing_item_id>", MainViews.edit_billing_item, name="edit_billing_item"),
    path("delete_billing_item/<billing_item_id>", MainViews.delete_billing_item, name="delete_billing_item"),

    # BILLING TEMPLATES
    path("manage_billing_templates", MainViews.manage_billing_templates, name="manage_billing_templates"),
    path("add_billing_template", MainViews.add_billing_template, name="add_billing_template"),
    path("add_billing_template_save", MainViews.add_billing_template_save, name="add_billing_template_save"),
    path("edit_billing_template/<billing_template_id>", MainViews.edit_billing_template, name="edit_billing_template"),
    path("delete_billing_template/<billing_template_id>", MainViews.delete_billing_template, name="delete_billing_template"),

    # STUDENT VIEWS
    # path("manage_billings/", MainViews.manage_billings, name="manage_billings"),
]