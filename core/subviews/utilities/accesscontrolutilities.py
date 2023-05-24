from django.shortcuts import render

# Creating restritive access wrappers
def is_admin(user):
    return user.is_superuser


def allow_user(*allowed_user_types):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Check if the user has any of the allowed user types
            if request.user.user_type not in allowed_user_types:
                previous_page = request.META.get('HTTP_REFERER')
                request.session['previous_page'] = previous_page
                context = {
                    "previous_page": previous_page
                }
                # Render the error page HTML
                return render(request, 'utility_templates/403.html', context, status=403)
            # User has the required permission, proceed to the view
            # if request.user.is_superuser:
            #     return view_func(request, *args, **kwargs)
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator