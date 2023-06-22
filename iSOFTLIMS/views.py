from django.shortcuts import render
from django.template import RequestContext
from iSOFTLIMS.utils.auth.password_reset import ForgotPasswordTokenGenerator

def handler404(request, exception):
    return render(request, "utility_templates/404.html", {})

def handler500(request, exception=None):
    return render(request, "utility_templates/500.html", {})
