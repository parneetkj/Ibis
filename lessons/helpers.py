from .models import Request, Booking

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
