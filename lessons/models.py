from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, StepValueValidator
from django.utils import timezone

class User(AbstractUser):
    """User model used for authentication and microblogs authoring."""

    username = models.EmailField(
        unique=True,
        blank = False,
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    is_student = models.BooleanField('student status', default = False)
    is_admin = models.BooleanField('admin status', default = False)
    is_director = models.BooleanField('director status', default = False)
    balance = models.FloatField(default=0)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def increase_balance(self,amount):
        self.balance += amount
        self.save()
        return self.balance
    def decrease_balance(self,amount):
        self.balance -= amount
        self.save()
        return self.balance


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

    day = models.CharField(max_length=10, blank=False)

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

    cost = models.FloatField(
        blank=False,
        default=5.00,
        validators=[
            StepValueValidator(
                limit_value=0.01,
                message="Cost must be max of two decimal places."
            )  
        ]
    )
    
    def generate_invoice(self):
        Invoice.objects.create(booking=self, total_price=self.get_price,date_paid=None, part_payment=0)
        self.student.decrease_balance(self.get_price)  

    def edit_invoice(self):
        invoice = Invoice.objects.get(booking=self)
        new_price = self.get_price()

        if(invoice.price < new_price):
            # The new price is more expensive than the original
            self.student.increase_balance(invoice.price)
            self.student.decrease_balance(new_price)
            invoice.price=new_price
            invoice.is_paid=False
            invoice.date_paid= None
            invoice.save()
        elif (invoice.price > new_price):
            # The new price is cheaper than the original payment
            self.student.increase_balance(invoice.price)
            self.student.decrease_balance(new_price)
            invoice.price=new_price
            invoice.save()

    @property
    def get_price(self):
        return round(self.cost*(60/self.duration)*self.no_of_lessons,2)

class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, blank=False)
    total_price = models.FloatField(blank=False)
    part_payment = models.FloatField(blank=True)
    is_paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(auto_now_add=True, blank=True, null=True)

