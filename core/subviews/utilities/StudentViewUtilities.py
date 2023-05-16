from core.models import DeferrmentApprovalWorklow , TemporaryWithdrawalApprovalWorklow

def check_student_is_defferred(student_id):
    # sourcery skip: inline-immediately-returned-variable
    student_exists = DeferrmentApprovalWorklow.objects.filter(applicant_id=student_id).exists()
    return student_exists

def check_student_is_temporarily_withdrawn(student_id):
    student_exists = TemporaryWithdrawalApprovalWorklow.objects.filter(applicant_id=student_id).exists()
    return student_exists