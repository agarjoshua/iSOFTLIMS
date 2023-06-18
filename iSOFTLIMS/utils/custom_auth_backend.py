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
            current_time = timezone.now()

            # Check if cooldown period has expired
            if user.login_attempts >= 5:
                cooldown_end_time = user.cooldown_end_time

                if cooldown_end_time and cooldown_end_time > current_time:
                    remaining_time = (cooldown_end_time - current_time).total_seconds() // 60
                    messages.error(request,f"Too many failed attempts. Please try again after {remaining_time} minutes.")
                    return None

                if cooldown_end_time and cooldown_end_time <= current_time:
                    user.login_attempts = 0
                    user.cooldown_end_time = None
                    user.save(update_fields=['login_attempts', 'cooldown_end_time'])

            if user.check_password(password):
                user.login_attempts = 0
                user.cooldown_end_time = None
                user.save(update_fields=['login_attempts', 'cooldown_end_time'])
                return user
            else:
                user.login_attempts += 1
                if user.login_attempts % 5 == 0:
                    cooldown_end_time = current_time + datetime.timedelta(minutes=5)
                    user.cooldown_end_time = cooldown_end_time
                user.save(update_fields=['login_attempts', 'cooldown_end_time'])
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
