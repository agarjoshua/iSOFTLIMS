from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from core.forms.applicantforms import ApplicantForm
from core.models import Applicant, ApplicantApprovalWorklow, CustomUser
from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test # type: ignore
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from core.utils.mail import EmailBackEnd


def is_applicant(user):
    return user.is_superuser or user.user_type==8


def applicantsignup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = CustomUser.objects.create_user(  # type: ignore
                username=email,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=8,
            )
            user.applicant.application_status = False
            user.save()
            messages.success(request, "You have been registered Successfully!")
            user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
            login(request, user)
            return redirect("applicant_home")
        except Exception as e:
            print(e)  # type: ignore
            messages.warning(request, f"error - {e}!")  # type: ignore
            return redirect("doSignUp")  # replace 'success' with your success URL
    else:
        form = ApplicantForm()

    context = {"form": form}
    return render(request, "application_form.html", context)


# @user_passes_test(is_applicant)
def applicant_home(request):
    # sourcery skip: extract-method, inline-immediately-returned-variable, remove-unnecessary-else, swap-if-else-branches
    
    applicant_form = ApplicantForm()
    # user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
    # login(request, user)
    user = request.user.id
    # applicant_obj = CustomUser.objects.get(id=user)
    # user = Applicant.objects.get(applicant=request.user.id)
    # user = CustomUser.objects.get(applicant=request.user.id)

    applicant = Applicant.objects.get(applicant=request.user.id)
    # has_paid = applicant.approval_workflow.finance_approved  # type: ignore

    try:
        has_applied = Applicant.objects.get(applicant=request.user.id).application_status
    except ObjectDoesNotExist as e:
        has_applied = False

    context = {
        "applicant_form": applicant_form,
        "has_applied": has_applied,
        #"has_paid": has_paid
    }

    if request.method == "POST":
        surname = request.POST.get("surname")
        other_names = request.POST.get("other_names")
        gender = request.POST.get("gender")
        nationality = request.POST.get("nationality")
        id_or_passport_number = request.POST.get("id_or_passport_number")
        date_of_birth = request.POST.get("date_of_birth")
        county = request.POST.get("county")
        telephone = request.POST.get("telephone")
        email = request.POST.get("email")
        current_address = request.POST.get("current_address")
        permanent_address = request.POST.get("permanent_address")
        special_needs = request.POST.get("special_needs")
        special_needs_description = request.POST.get("special_needs_description")


        programme_level = request.POST.get("programme_level")
        degree_name = request.POST.get("degree_name")
        field_of_study = request.POST.get("field_of_study")
        faculty = request.POST.get("faculty")
        department = request.POST.get("department")
        concept_paper = request.FILES.get("concept_paper")
        masters_degree_type = request.POST.get("masters_degree_type")
        masters_degree_title = request.POST.get("masters_degree_title")
        start_date = request.POST.get("start_date")
        expected_completion_date = request.POST.get("expected_completion_date")
        mode_of_study = request.POST.get("mode_of_study")
        photo_1 = request.FILES.get("photo_1")
        photo_2 = request.FILES.get("photo_2")
        secondary_schools_attended = request.POST.get("secondary_schools_attended")
        university_education = request.POST.get("university_education")
        other_degrees_or_diploma = request.POST.get("other_degrees_or_diploma")
        research_experience = request.POST.get("research_experience")
        employment_work_experience = request.POST.get("employment_work_experience")
        languages_spoken = request.POST.get("languages_spoken")

        
        referee1_name = request.POST.get("referee1_name")
        referee1_designation = request.POST.get("referee1_designation")
        referee1_address = request.POST.get("referee1_address")
        referee1_telephone = request.POST.get("referee1_telephone")
        referee1_email = request.POST.get("referee1_email")
        referee2_name = request.POST.get("referee2_name")
        referee2_designation = request.POST.get("referee2_designation")
        referee2_address = request.POST.get("referee2_address")
        referee2_telephone = request.POST.get("referee2_telephone")
        referee2_email = request.POST.get("referee2_email")
        how_did_you_know_about_us = request.POST.get("how_did_you_know_about_us")

        # user = request.user.id
        # applicant_obj = CustomUser.objects.get(id=user)

        try:
            # Update the instance of the Applicant model
            applicant = Applicant.objects.get(applicant=request.user.id)
            applicant.surname=surname
            applicant.other_names=other_names
            applicant.gender=gender
            applicant.nationality=nationality
            applicant.id_or_passport_number=id_or_passport_number
            applicant.date_of_birth=date_of_birth
            applicant.county=county
            applicant.telephone=telephone
            applicant.email=email
            applicant.current_address=current_address
            applicant.permanent_address=permanent_address
            applicant.special_needs=special_needs
            applicant.special_needs_description=special_needs_description
            applicant.programme_level=programme_level
            applicant.degree_name=degree_name
            applicant.field_of_study=field_of_study
            applicant.faculty=faculty
            applicant.department=department
            applicant.concept_paper=concept_paper
            applicant.masters_degree_type=masters_degree_type
            applicant.masters_degree_title=masters_degree_title
            applicant.start_date=start_date
            applicant.expected_completion_date=expected_completion_date
            applicant.mode_of_study=mode_of_study
            applicant.photo_1=photo_1 
            applicant.photo_2=photo_2


            applicant.secondary_schools_attended=secondary_schools_attended
            applicant.university_education=university_education
            applicant.other_degrees_or_diploma=other_degrees_or_diploma
            applicant.research_experience=research_experience
            applicant.employment_work_experience=employment_work_experience
            applicant.languages_spoken=languages_spoken
            applicant.referee1_name=referee1_name
            applicant.referee1_designation=referee1_designation
            applicant.referee1_address=referee1_address
            applicant.referee1_telephone=referee1_telephone
            applicant.referee1_email=referee1_email
            applicant.referee2_name=referee2_name
            applicant.referee2_designation=referee2_designation
            applicant.referee2_address=referee2_address
            applicant.referee2_telephone=referee2_telephone
            applicant.referee2_email=referee2_email
            applicant.how_did_you_know_about_us=how_did_you_know_about_us
            applicant.application_status = True
            applicant.save()
            approval_worklow_initiate = ApplicantApprovalWorklow.objects.create(
                applicant = applicant
            )
            approval_worklow_initiate.save()
            messages.success(request, 'Application sent successfully and approval process initiated')
            return redirect('applicant_home')
        # except IntegrityError as e:
        #     messages.error(request, 'Application not sent (Possibly because youve already applied)')
        #     return redirect('applicant_home')
        except Exception as e:
            messages.error(request, f'Application not sent successfully because - {e}')
            return redirect('applicant_home')
    else:
        form = ApplicantForm()

    # context = {'form': form}
    # return render(request, 'application_form.html', context)
    return render(request, "applicant_templates/applicant_home_template.html", context)
