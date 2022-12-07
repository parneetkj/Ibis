from .models import Request, Booking, Transfer, Invoice, User
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone

def get_user_requests(user):
    requests = Request.objects.filter(student=user)
    return requests

def get_all_requests():
    requests = Request.objects.filter()
    return requests

def get_user_bookings(user):
    bookings = Booking.objects.filter(student=user)
    return bookings

def get_all_bookings():
    bookings = Booking.objects.filter()
    return bookings

def get_user_invoices(user):
    user_bookings = get_user_bookings(user)
    user_invoices = Invoice.objects.filter(booking__in=user_bookings)
    return user_invoices

def get_user_transfers(user):
    user_invoices = get_user_invoices(user)
    user_transfers = Transfer.objects.filter(invoice__in=user_invoices)
    return user_transfers

def get_invoice_transfers(invoice):
    return Transfer.objects.filter(invoice=invoice)

def create_transfer(invoice,amount):
    Transfer.objects.create(invoice=invoice,amount=amount)
    invoice.add_partial_payment(amount)

def calculate_student_balance(user):
    user_invoices = get_user_invoices(user)

    total_bill = 0
    total_paid = 0
    for invoice in user_invoices:
        total_bill += invoice.total_price
        total_paid += invoice.partial_payment

    user.set_balance(round(total_paid-total_bill,2))
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
