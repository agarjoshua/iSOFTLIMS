from django.utils import timezone

class SessionIdleTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            current_time = timezone.now()

            if last_activity is not None and (current_time - last_activity).total_seconds() > 600:
                # User has been idle for more than 10 minutes, logout the user
                from django.contrib.auth import logout
                logout(request)

            # Update last activity time
            request.session['last_activity'] = current_time

        response = self.get_response(request)
        return response
