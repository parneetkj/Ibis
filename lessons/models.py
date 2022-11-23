from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db.models import TimeField, DateTimeField

# Create your models here.



class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)


class Request(models.Model):
    """Requests by students"""

    student = models.CharField(max_length=50, blank=False)
    availability = models.CharField(max_length=200, blank=False)
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
        (15, '15 Minuite'),
        (30, '30 Minuite'),
        (45, '45 Minuite'),
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
    (15, '15 Minuite'),
    (30, '30 Minuite'),
    (45, '45 Minuite'),
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

    def generate_invoice():
        pass
