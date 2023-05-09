from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.shortcuts import render, redirect

from finance.models import Fee, Transaction, Transactiontype
from .forms.finance import FeeCreationForm, TransactionForm
from django.contrib import messages
from core.models import Admin, Applicant, ApplicantApprovalWorklow, Guardian, Students

# from .models import Fee, Transaction

# TODO: Global prefetched objects
def finance_home(request):
    all_application_payments = Applicant.objects.all()
    all_applications_count = Applicant.objects.all().count()
    

    context = {
        "all_application_payments" : all_application_payments,
        "all_applications_count": all_applications_count,
    }
    return render(request, "finance/finance_home.html", context)



def approve_applications(request):
    all_application_payments = Applicant.objects.all()
    transaction_type = Transactiontype.objects.get(name__icontains='Application Fees')
    all_application_transactions = Transaction.objects.filter(transaction_type=transaction_type)

    applicant_approval_workflow = ApplicantApprovalWorklow.objects.all()

    approved_applicants = Applicant.objects.filter(applicantapprovalworklow__finance_approved=True)

    context = {
        "all_application_payments" : all_application_payments,
        "all_application_transactions": all_application_transactions,
        "applicant_approval_workflow":applicant_approval_workflow,
        "approved_applicants":approved_applicants
    }
    return render(request, "finance/applicant_finance.html", context)


def approve(request):
    
    applicant_id = request.POST.get("selected_id")
    print(applicant_id)
    applicant = Applicant.objects.get(applicant_id=applicant_id)
    print(applicant)
    selected_applicant = ApplicantApprovalWorklow.objects.get(applicant=applicant)

    try:
        selected_applicant = ApplicantApprovalWorklow.objects.get(applicant=applicant)
        selected_applicant.finance_approved = True
        selected_applicant.save()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(e)

def create_fee_template(request):
    if request.method == "POST":
        form = FeeCreationForm(request.POST)
        if form.is_valid():
            try:
                current_user = request.user.id
                test = Admin.objects.get(user_id=current_user)
                feeform = form.save(commit=False)
                feeform.editor = test
                feeform.save()

            except Exception as e:
                print(e)
            messages.success(request, "Creation successful.")
            return redirect("finance:pay")
        messages.error(request, "Unsuccessful creation. Invalid information.")
    form = FeeCreationForm()

    return render(
        request=request,
        template_name="finance/index.html",
        context={"fee_creation_form": form},
    )


def bill(request, id):

    fee = Fee.objects.get(id=id)
    all_students = Students.objects.all()

    for i in all_students:
        try:
            i.account_balance -= fee.ammount
            Transaction.objects.create(
                student=i,
                transaction_details=fee.name,
            )
            i.save()
        except Exception as e:
            print(e)
    fee.billed = True
    fee.save()

    return redirect("finance:pay")


def pay(request):
    if request.method == "POST":
        if form.is_valid():
            try:
                student = form.cleaned_data.get("student")
                type_of_payment = form.cleaned_data.get("type_of_payment")
                form_of_payment = form.cleaned_data.get("form_of_payment")
                ammount_paid = form.cleaned_data.get("ammount")

                billed_student = (
                    Students.objects.filter(admission_number=student).first().user_id
                )
                student = billed_student
                print(billed_student)
                print(student)
                try:
                    transaction = Transaction.objects.create(
                        ammount_paid,
                        student=billed_student,
                        type=type_of_payment,
                        form_of_payment=form_of_payment,
                    )
                except ValueError as e:
                    print(e)
                    return messages.error(
                        request, "You have entered an invalid admission number."
                    )

                if not transaction:
                    return messages.error(
                        request, "Something went wrong with your request."
                    )

            except Exception as e:
                print(e)
            messages.success(request, "Creation successful.")
            return redirect("finance:home")
        messages.error(request, "Unsuccessful creation. Invalid information.")
    form = FeeCreationForm()

    return redirect("finance:home")


#########################################UTILITIES#######################################################################


@csrf_exempt
def check_student_exist(request):
    username = request.POST.get("id_student")
    print(username)
    user_obj = Students.objects.filter(admission_number=username).exists()
    print("=========================================================")
    print(user_obj)
    print("=========================================================")
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
