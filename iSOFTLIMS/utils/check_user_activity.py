from functools import wraps
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import logout
from django.utils import timezone

def check_user_activity(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            # current_time = timezone.now()

            if last_activity is None:
                # User has been idle for more than 10 minutes, log them out
                logout(request)
                messages.warning(request, 'User has been signed out due to inactivity.')

                # Convert datetime to string representation
                # last_activity_str = last_activity.strftime('%Y-%m-%d %H:%M:%S')

                return render(request, 'login.html')

            # Update last activity time
            # request.session['last_activity'] = current_time

        return view_func(request, *args, **kwargs)

    return wrapper
