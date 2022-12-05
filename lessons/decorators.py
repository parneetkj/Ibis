from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings

def student_required(view_function):

    # Decorator for views that checks that the logged in user is a student,
    # redirects to the feed page if not and displays an error message.

    def modified_view_function(request, *args, **kwargs):
        if request.user.is_admin:
            messages.add_message(request, messages.ERROR, "You cannot access this page!")
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request, *args, **kwargs)
    return modified_view_function


   
def admin_required(view_function): 
    # Decorator for views that checks that the logged in user is an admin,
    # redirects to the feed page if not.

    def modified_view_function(request, *args, **kwargs):
        if request.user.is_student:
            messages.add_message(request, messages.ERROR, "You cannot access this page!")
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request, *args, **kwargs)
    return modified_view_function


def director_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='log_in'):

    # Decorator for views that checks that the logged in user is an admin,
    # redirects to the log-in page if not.


    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_director,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
