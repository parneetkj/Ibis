from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
#from django.shortcuts import redirect

def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='log_in'):

    # Decorator for views that checks that the logged in user is a student,
    # redirects to the log-in page if not.


    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_student,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='log_in'):

    # Decorator for views that checks that the logged in user is an admin,
    # redirects to the log-in page if not.

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_admin,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        #messages.add_message(redirect_field_name, messages.ERROR, "You cannot access this page!")
        #return redirect('feed')
        return actual_decorator(function)
    else:
        
        return actual_decorator

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
