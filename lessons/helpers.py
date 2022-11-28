from .models import Request, Booking, User
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

def get_requests(user):
    # To do: Change to user when implemented
    requests = Request.objects.filter(student=user)
    return requests

def get_users_bookings(user):
    # To do: Change to user when implemented
    bookings = Booking.objects.filter(student=user)
    return bookings

def get_all_bookings():
    # To do: Change to user when implemented
    bookings = Booking.objects.filter()
    return bookings

def admin_required(view_function):
    def modified_view_function(request, *args, **kwargs):
        if request.user.is_student:
            messages.add_message(request, messages.ERROR, "You cannot access this page!")
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request, *args, **kwargs)
    return modified_view_function

