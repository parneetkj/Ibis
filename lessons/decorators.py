from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings

def student_required(view_function):

    # Decorator for views that checks that the logged in user is a student,
    # redirects to the feed page if not and displays an error message.

    def modified_view_function(request, *args, **kwargs):
        if request.user.is_student:
            return view_function(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, "You cannot access this page!")
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    return modified_view_function



def admin_required(view_function):
    # Decorator for views that checks that the logged in user is an admin or a director,
    # redirects to the feed page if not.

    def modified_view_function(request, *args, **kwargs):
        if request.user.is_admin or request.user.is_director:
            return view_function(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, "You cannot access this page!")
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    return modified_view_function


def director_required(view_function):

    # Decorator for views that checks that the logged in user is a director,
    # redirects to the feed page if not and displays an error message.

    def modified_view_function(request, *args, **kwargs):
        if request.user.is_director:
            return view_function(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, "You cannot access this page!")
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    return modified_view_function
