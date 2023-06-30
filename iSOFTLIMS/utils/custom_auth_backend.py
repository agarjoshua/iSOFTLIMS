import datetime
from django.utils import timezone
from django.utils.timezone import make_aware


from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.messages import constants as message_constants

User = get_user_model()
class EmailMaxLoginAttemptsBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)

            if user.account_status == 'Deactivated':
                print("deactivated")
                messages.error(request, "Your account has been deactivated. Please click activate to start the activation process.")
                return None

            if user.login_attempts >= 3:
                user.account_status = 'Deactivated'
                messages.error(request, "Too many failed attempts. Your account has been temporarily locked.")
                user.save(update_fields=['account_status'])
                return None

            if user.check_password(password):
                user.login_attempts = 0
                user.save(update_fields=['login_attempts'])
                return user
            else:
                user.login_attempts += 1
                user.save(update_fields=['login_attempts'])
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None