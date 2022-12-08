from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from lessons.models import User, Request, Booking, Transfer, Invoice
from random import randint, random
from decimal import Decimal
from lessons.helpers import create_transfer, calculate_student_balance

#import pytz

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 100
    REQUEST_COUNT = 50
    BOOKING_COUNT = 100
    PAID_PROBABILITY = 0.75
    OVER_PAID_PROBABILITY = 0.1
    PARTIAL_PAID_PROBABILITY = 0.25


    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()
        self.create_admin("Petra", "Pickles")
        self.create_admin("David", "Dawson")
        self.create_director("Marty", "Major")

        self.students = User.objects.all().filter(is_student=True)

        self.create_requests()
        self.create_bookings()

    def create_users(self):
        self.create_user("John", "Doe")
        user_count = 1
        while user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            try:
                first_name = self.faker.first_name()
                last_name = self.faker.last_name()
                self.create_user(first_name, last_name)
            except:
                continue
            user_count += 1
        print("User seeding complete.      ")

    def create_user(self, first_name, last_name ):
        username = self.email(first_name, last_name)
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
            is_student=True
        )

    def create_admin(self, first_name, last_name ):
        username = self.email(first_name, last_name)
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
            is_admin=True
        )
    
    def create_director(self, first_name, last_name ):
        username = self.email(first_name, last_name)
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
            is_admin=True,
            is_director=True
        )

    def create_requests(self):
        for i in range(self.REQUEST_COUNT):
            print(f"Seeding requests {i}/{self.REQUEST_COUNT}", end='\r')
            self.create_request()
        print("Request seeding complete.      ")

    def create_request(self):
        request = Request(
            student=self.get_random_student(),
            date="2023-12-12",
            time="10:51",
            amount=randint(1,50),
            interval=randint(1,4),
            duration=60,
            topic = "Topic",
            teacher = "Ms.Test",
        )
        request.save()

    def create_bookings(self):
        for i in range(self.BOOKING_COUNT):
            print(f"Seeding booking {i}/{self.BOOKING_COUNT}", end='\r')
            self.create_booking()
        print("Booking seeding complete.      ")

    def create_booking(self):
        booking = Booking(
            student=self.get_random_student(),
            day="Monday",
            start_date="2023-12-12",
            time="10:51",
            no_of_lessons=randint(1,50),
            interval=randint(1,4),
            duration=60,
            topic = "Topic",
            teacher = "Ms.Test",
            cost=randint(1,20)
        )
        booking.save()
        booking.generate_invoice()
        booking_invoice = Invoice.objects.get(booking=booking)
        if random() < self.PAID_PROBABILITY:
            self.pay_invoice(booking_invoice)
        
        calculate_student_balance(booking.student)

    def pay_bookings(self):
        for i in range(self.BOOKING_COUNT):
            print(f"Adding Payment {i}/{self.BOOKING_COUNT}", end='\r')
            self.pay_booking()
        print("Payment seeding complete.      ")

    def pay_invoice(self, invoice):
        random_num = random()
        if random_num < self.OVER_PAID_PROBABILITY:
            pay_amount = invoice.total_price * Decimal(1.2)
        elif random_num < self.PARTIAL_PAID_PROBABILITY:
            pay_amount = invoice.total_price * Decimal(0.5)
        else:
            pay_amount = invoice.total_price
        
        #invoice.add_partial_payment(pay_amount)
        create_transfer(invoice, pay_amount)
        invoice.check_if_paid()
        invoice.change_invoice_amount()

        

    def get_random_student(self):
        index = randint(0,self.students.count()-1)
        return self.students[index]

    def email(self, first_name, last_name):
        email = f'{first_name.lower()}.{last_name.lower()}@example.org'
        return email