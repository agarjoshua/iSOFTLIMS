from academics.forms.sessionforms import SessionEditForm
from django.shortcuts import render, redirect
from academics.models import Session
from django.contrib import messages
from core.subviews.utilities.accesscontrolutilities import allow_user
# from core.forms import AddStudentForm, EditStudentForm
from django.db import DatabaseError, IntegrityError, DataError, OperationalError, ProgrammingError

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

    if sort_by := request.GET.get('sort'):
        session_years = session_years.order_by(sort_by)

    context = {
        "session_years": session_years,
        }
    return render(request, "session_templates/manage_session_template.html", context)


def add_session(request):
    return render(request, "session_templates/add_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("academics:add_session")
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
            return redirect("academics:manage_session")
        except Exception as e:
            messages.error(request, f"Failed to Add Session Year (i.e {e})")
            return redirect("add_session")


def edit_session(request, session_id):
    selected_session = Session.objects.get(id=session_id)
    if request.method == 'POST':
        form = SessionEditForm(request.POST, instance=selected_session)
        if form.is_valid():
            try: 
                form.save()
                messages.success(request, "Session edited Successfully.")
                return redirect("academics:manage_session")
            except Exception as e:
                messages.error(request, f"Failed to Edit Session. bacause {e}")
                form = SessionEditForm(instance=selected_session)

        else:
            errors = form.errors
            print(errors) 
            messages.error(request, "Failed to Edit Session. Form isnt valid")
            return _edit_sessions_helper(selected_session, session_id, request)
    else:
        _edit_sessions_helper(selected_session, session_id, request)

    return _edit_sessions_helper(selected_session, session_id, request)

def _edit_sessions_helper(selected_session, session_id, request):
    form = SessionEditForm(instance=selected_session)
    context = {'form': form, 'selected_session': selected_session, "id": session_id}
    return render(request, "session_templates/edit_session_template.html", context)


def delete_session(request, session_id):
    session = Session.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect("academics:manage_session")
    except Exception as e:
        messages.error(request, f"Failed to Delete Session. {e}")
        return redirect("academics:manage_session")
