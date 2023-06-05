from django.shortcuts import render, redirect
from academics.models import Session
from django.contrib import messages
from core.subviews.utilities.accesscontrolutilities import allow_user
# from core.forms import AddStudentForm, EditStudentForm

# USER NUMBER REFERENCE
# 1 = ADMIN
# 2 = STAFF
# 3 = STUDENTS
# 4 = HOD
# 5 = GUARDIAN
# 6 = TEACHER
 


@allow_user('1','2','3','4','5','6') 
def manage_session(request):
    session_years = Session.objects.all()
    context = {"session_years": session_years}
    return render(request, "session_templates/manage_session_template.html", context)


def add_session(request):
    return render(request, "session_templates/add_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("add_session")
    else:
        session_start_date = request.POST.get("session_start_date")
        session_end_date = request.POST.get("session_end_date")
        is_current = request.POST.get("is_current") == "on"

        if is_current:
            Session.objects.all().update(is_current=False)

        try:
            sessionyear = Session(
                session_start_date=session_start_date, 
                session_end_date=session_end_date,
                is_current = is_current
            )
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("manage_session")
        except exceptions.ValidationError as e:
            messages.error(
                request,
                f"Failed to Add Session Year Due to incomplete or incorrect entry of fields (i.e {e})",
            )
            return redirect("manage_session")
        except Exception as e:
            messages.error(request, f"Failed to Add Session Year (i.e {e})")
            return redirect("add_session")


def edit_session(request, session_id):
    session_year = Session.objects.get(id=session_id)
    context = {"session_year": session_year}
    return render(request, "session_templates/edit_session_template.html", context)


def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("manage_session")
    else:
        session_id = request.POST.get("session_id")
        session_start_year = request.POST.get("session_start_year")
        session_end_year = request.POST.get("session_end_year")
        is_current = request.POST.get("is_current") == "on"

        if is_current:
            Session.objects.all().update(is_current=False)

        try:
            session_year = Session.objects.get(id=session_id)
            session_year.session_start_date = session_start_year
            session_year.session_end_date = session_end_year
            session_year.is_current = is_current
            print(session_year)
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect("/edit_session/" + session_id)
        except Exception as e:
            messages.error(request, f"Failed to Update Session Year. -{e}")
            return redirect("/edit_session/" + session_id)


def delete_session(request, session_id):
    session = Session.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect("manage_session")
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect("manage_session")
