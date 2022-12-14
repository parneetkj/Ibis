from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, StepValueValidator, DecimalValidator
from decimal import Decimal
from django.utils import timezone
class User(AbstractUser):
    """User model used for authentication and lessons authoring."""

    username = models.EmailField(
        unique=True,
        blank = False,
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    is_student = models.BooleanField('student status', default = False)
    is_admin = models.BooleanField('admin status', default = False)
    is_director = models.BooleanField('director status', default = False)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def set_balance(self,amount):
        self.balance = amount
        self.save()

class Request(models.Model):
    """Requests by students"""

    student = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateField(
        blank=False,
    )

    time = models.TimeField(
        blank=False,
    )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=1,
                message="Must book at least 1 lesson."
            ),
            MaxValueValidator(
                limit_value=50,
                message="Cannot book more than 50 lessons."
            )
        ]
    )
    interval = models.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=1,
                message="Must book at least 1 week of lessons."
            ),
            MaxValueValidator(
                limit_value=4,
                message="Interval cannot be more than a month."
            )
        ]
    )
    DURATION_CHOICES = [
        (15, '15 Minute'),
        (30, '30 Minute'),
        (45, '45 Minute'),
        (60, '1 Hour'),
    ]
    duration = models.IntegerField(
        choices=DURATION_CHOICES,
        default=30
    )
    topic = models.CharField(
        max_length=50,
        default="Any",
        blank=True
    )
    teacher = models.CharField(
        max_length=100,
        default="Any",
        blank=True
    )
    status = models.CharField(
        max_length=20,
        default = "In Progress"
    )

class Booking(models.Model):
    """ Booking by admin """

    student = models.ForeignKey(User, on_delete=models.CASCADE)

    DAY_CHOICES = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
    ]
    day = models.CharField(max_length=10, blank=False, choices=DAY_CHOICES)

    time = models.TimeField(blank=False)

    start_date = models.DateField(blank=False)

    DURATION_CHOICES = [
    (15, '15 Minute'),
    (30, '30 Minute'),
    (45, '45 Minute'),
    (60, '1 Hour'),
    ]
    duration = models.IntegerField(
    choices=DURATION_CHOICES,
    default=30,
    blank=False
    )

    interval = models.IntegerField(
        blank=False,
        validators=[
            MinValueValidator(
                limit_value=1,
                message="Must book at least 1 week of lessons."
            ),
            MaxValueValidator(
                limit_value=4,
                message="Interval cannot be more than a month."
            )
        ]
    )

    teacher = models.CharField(
        max_length=100,
        blank=False
    )

    no_of_lessons = models.IntegerField(
        blank=False,
        validators=[
            MinValueValidator(
                limit_value=1,
                message="Must book at least 1 lesson."
            ),
            MaxValueValidator(
                limit_value=50,
                message="Cannot book more than 50 lessons."
            )
        ]
    )

    topic = models.CharField(
        max_length=50,
        blank=False
    )

    cost = models.DecimalField(
        blank=False,
        max_digits=10,
        decimal_places=2
    )

    def generate_invoice(self):
        Invoice.objects.create(booking=self, total_price=self.get_price,date_paid=None)

    @property
    def get_price(self):
        return Decimal(float(self.cost)*(60/self.duration)*self.no_of_lessons)

class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, blank=False)
    total_price = models.DecimalField(blank=False, max_digits=10, decimal_places=2)
    partial_payment = models.DecimalField(default=0 ,max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    def add_partial_payment(self,amount):
        self.partial_payment += amount
        self.save()
    def check_if_paid(self):
        if self.partial_payment >= self.total_price:
            self.is_paid = True
            self.date_paid = timezone.now()
            self.save()

    def change_invoice_amount(self):
        self.total_price = self.booking.get_price
        if self.partial_payment < self.total_price:
            self.is_paid = False
            self.date_paid = None
        elif self.partial_payment >= self.total_price:
            self.is_paid = True
            self.date_paid = timezone.now()
        self.save()

class Transfer(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(blank=False, max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True, blank=False)
