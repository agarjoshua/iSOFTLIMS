# handle all needed imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from finance.forms.billingtemplatesforms import BillingTemplateForm, EditBillingTemplateForm
from finance.forms.billingitemform import BillingItemForm, UpdateBillingItemForm
from finance.forms.paymentforms import BankForm, BankUpdateForm, PaymentMethodsForm, PaymentMethodsUpdateForm
from finance.models import PaymentMethods, Bank, BillingItem, BillingTemplate
from django.contrib.auth.decorators import login_required


######################################### PAYMENT METHODS & BANK ############################################################

def manage_payment_methods(request):
    payment_methods = PaymentMethods.objects.all()
    context = {
        "payment_methods" : payment_methods
    }
    return render(request, 'finance/manage_payment_methods_template.html', context)

def add_payment_method(request):
    form = PaymentMethodsForm()
    context = {
        "form":form
    }
    return render(request, 'finance/add_payment_method_template.html', context)

def add_payment_method_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("finance:manage_payment_methods")
    else:
        form = PaymentMethodsForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Payment Method Added Successfully!")
                return redirect("finance:manage_payment_methods")
            except Exception as e:
                messages.error(request, f"Failed to Add Payment Method - {e}!")
                return redirect("finance:add_payment_method")
        else:
            error_message = "Form is not valid. Please check the following issues:\n"
            for field, errors in form.errors.items():
                error_message += f"{field}: {', '.join(errors)}"
            messages.error(request, error_message)
            return redirect("finance:add_payment_method")
        
def edit_payment_method(request, payment_method_id):
    payment_method = get_object_or_404(PaymentMethods, id=payment_method_id) 
    print(payment_method)
    edit_payment_method_form = PaymentMethodsUpdateForm(instance=payment_method)

    if request.method == 'POST':
        form = PaymentMethodsUpdateForm(request.POST, instance=payment_method)
        if form.is_valid():
            form = form.save()
            PaymentMethodsUpdateForm(instance=payment_method)
            messages.success(request,'Payment Method Updated Succesfully')
            return redirect("finance:manage_payment_methods")
    context = {
        'edit_payment_methods_form' : edit_payment_method_form
    }
    return render(request, 'finance/edit_payment_method_template.html', context)

def delete_payment_method(request, payment_method_id):
    payment_method = PaymentMethods.objects.get(id=payment_method_id)
    try:
        payment_method.delete()
        messages.warning(request, "Payment Method Deleted Successfully.")
        return redirect("finance:manage_payment_methods")
    except:
        messages.error(request, "Failed to Delete Payment Method!")
        return redirect("finance:manage_payment_methods")
    
def manage_banks(request):
    banks = Bank.objects.all()
    context = {
        "banks" : banks
    }
    return render(request, 'finance/manage_banks_template.html', context)

def add_bank(request):
    form = BankForm()
    context = {
        "form":form
    }
    return render(request, 'finance/add_bank_template.html', context)

def add_bank_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("finance:manage_banks")
    else:
        form = BankForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Bank Added Successfully!")
                return redirect("finance:manage_banks")
            except Exception as e:
                messages.error(request, f"Failed to Add Bank - {e}!")
                return redirect("finance:add_bank")
        else:
            error_message = "Form is not valid. Please check the following issues:\n"
            for field, errors in form.errors.items():
                error_message += f"{field}: {', '.join(errors)}"
            messages.error(request, error_message)
            return redirect("finance:add_bank")
        

def edit_bank(request, bank_id):
    bank = get_object_or_404(Bank, id=bank_id) 
    edit_bank_form = BankUpdateForm(instance=bank)

    if request.method == 'POST':
        form = BankUpdateForm(request.POST, instance=bank)
        if form.is_valid():
            form = form.save()
            BankUpdateForm(instance=bank)
            messages.success(request,'Bank Updated Succesfully')
            return redirect("finance:manage_banks")
    context = {
        'edit_bank_form' : edit_bank_form
    }
    return render(request, 'finance/edit_bank_template.html', context)

def delete_bank(request, bank_id):
    bank = Bank.objects.get(id=bank_id)
    try:
        bank.delete()
        messages.warning(request, "Bank Deleted Successfully.")
        return redirect("finance:manage_banks")
    except:
        messages.error(request, "Failed to Delete Bank!")
        return redirect("finance:manage_banks")
    


######################################### billing ITEMS #######################################################################

def manage_billing_items(request):
    billing_items = BillingItem.objects.all()
    context = {
        "billing_items" : billing_items
    }
    return render(request, 'finance/manage_billing_items_template.html', context)

def add_billing_item(request):
    form = BillingItemForm()
    context = {
        "form":form
    }
    return render(request, 'finance/add_billing_item_template.html', context)

def add_billing_item_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("finance:manage_billing_items")
    else:
        form = BillingItemForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "billing Item Added Successfully!")
                return redirect("finance:manage_billing_items")
            except Exception as e:
                messages.error(request, f"Failed to Add billing Item - {e}!")
                return redirect("finance:add_billing_item")
        else:
            error_message = "Form is not valid. Please check the following issues:\n"
            for field, errors in form.errors.items():
                error_message += f"{field}: {', '.join(errors)}"
            messages.error(request, error_message)
            return redirect("finance:add_billing_item")
        

def edit_billing_item(request, billing_item_id):
    billing_item = get_object_or_404(BillingItem, id=billing_item_id) 
    edit_billing_item_form = UpdateBillingItemForm(instance=billing_item)

    if request.method == 'POST':
        form = UpdateBillingItemForm(request.POST, instance=billing_item)
        if form.is_valid():
            form = form.save()
            UpdateBillingItemForm(instance=billing_item)
            messages.success(request,'billing Item Updated Succesfully')
            return redirect("finance:manage_billing_items")
    context = {
        'edit_billing_item_form' : edit_billing_item_form
    }
    return render(request, 'finance/edit_billing_item_template.html', context)


def delete_billing_item(request, billing_item_id):
    billing_item = BillingItem.objects.get(id=billing_item_id)
    try:
        billing_item.delete()
        messages.warning(request, "billing Item Deleted Successfully.")
        return redirect("finance:manage_billing_items")
    except:
        messages.error(request, "Failed to Delete billing Item!")
        return redirect("finance:manage_billing_items")
    



#########################################   BILLING TEMPLATES   #######################################################################
def manage_billing_templates(request):
    billing_templates = BillingTemplate.objects.all()
    context = {
        "billing_templates" : billing_templates
    }
    return render(request, 'finance/manage_billing_templates_template.html', context)

def add_billing_template(request):
    form = BillingTemplateForm()
    context = {
        "form":form
    }
    return render(request, 'finance/add_billing_template_template.html', context)

def add_billing_template_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("finance:manage_billing_templates")
    else:
        form = BillingTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Billing Template Added Successfully!")
                return redirect("finance:manage_billing_templates")
            except Exception as e:
                messages.error(request, f"Failed to Add Billing Template - {e}!")
                return redirect("finance:add_billing_template")
        else:
            error_message = "Form is not valid. Please check the following issues:\n"
            for field, errors in form.errors.items():
                error_message += f"{field}: {', '.join(errors)}" 
            messages.error(request, error_message)
            return redirect("finance:add_billing_template")

def edit_billing_template(request, billing_template_id):
    billing_template = get_object_or_404(BillingTemplate, id=billing_template_id) 
    edit_billing_template_form = EditBillingTemplateForm(instance=billing_template)

    if request.method == 'POST':
        form = EditBillingTemplateForm(request.POST, instance=billing_template)
        if form.is_valid():
            form = form.save()
            EditBillingTemplateForm(instance=billing_template)
            messages.success(request,'Billing Template Updated Succesfully')
            return redirect("finance:manage_billing_templates")
    context = {
        'edit_billing_template_form' : edit_billing_template_form
    }
    return render(request, 'finance/edit_billing_template_template.html', context)

def delete_billing_template(request, billing_template_id):
    billing_template = BillingTemplate.objects.get(id=billing_template_id)
    try:
        billing_template.delete()
        messages.warning(request, "Billing Template Deleted Successfully.")
        return redirect("finance:manage_billing_templates")
    except:
        messages.error(request, "Failed to Delete Billing Template!")
        return redirect("finance:manage_billing_templates")
    
