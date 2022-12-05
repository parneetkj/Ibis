from .models import Request, Booking
from django.conf import settings
from django.shortcuts import redirect

def get_requests(user):
    # To do: Change to user when implemented
    requests = Request.objects.filter(student=user)
    return requests

def get_users_bookings(user):
    # To do: Change to user when implemented
    bookings = Booking.objects.filter(student=user)
    return bookings



class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

def get_all_bookings():
    # To do: Change to user when implemented
    bookings = Booking.objects.filter()
    return bookings

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function
