from django.core.management.base import BaseCommand, CommandError
from lessons.models import User, Request, Booking, Invoice, Transfer

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.filter().delete()
        Request.objects.filter().delete()
        Booking.objects.filter().delete()
        Invoice.objects.filter().delete()
        Transfer.objects.filter().delete()