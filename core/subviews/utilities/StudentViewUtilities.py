from core.models import HOD, DeferrmentApprovalWorklow , TemporaryWithdrawalApprovalWorklow

def check_student_is_defferred(student_id):
    # sourcery skip: inline-immediately-returned-variable
    student_exists = DeferrmentApprovalWorklow.objects.filter(applicant_id=student_id).exists()
    return student_exists

def check_student_is_temporarily_withdrawn(student_id):
    student_exists = TemporaryWithdrawalApprovalWorklow.objects.filter(applicant_id=student_id).exists()
    return student_exists

def check_hod_type(user):
    try:
        hod = HOD.objects.get(admin_id=user)
        return hod.hod_type
    except HOD.DoesNotExist:
        return None