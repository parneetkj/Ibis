from .models import Request, Booking, Transfer, Invoice, User
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone

def get_user_requests(user):
    # To do: Change to user when implemented
    requests = Request.objects.filter(student=user)
    return requests

def get_all_requests():
    # To do: Change to user when implemented
    requests = Request.objects.filter()
    return requests

def get_user_bookings(user):
    # To do: Change to user when implemented
    bookings = Booking.objects.filter(student=user)
    return bookings

def get_all_bookings():
    # To do: Change to user when implemented
    bookings = Booking.objects.filter()
    return bookings

def get_all_transfers():
    return Transfer.objects.all()

def check_for_refund(booking):
    invoice = Invoice.objects.get(booking=booking)
    if invoice.is_paid:
        booking.student.increase_balance(invoice.total_price)
class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function
