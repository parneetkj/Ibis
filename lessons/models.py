from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
# Create your models here.

class User(AbstractUser):

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    is_student = models.BooleanField('student status', default = False)
    is_admin = models.BooleanField('admin status', default = False)
    is_director = models.BooleanField('director status', default = False)


class Request(models.Model):
    """Requests by students"""

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    
    date = models.DateField(
        blank=False,
        default= timezone.now()
    )

    time = models.TimeField(
        blank=False,
        default= timezone.now()
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

    student = models.CharField(max_length=50, blank=False)

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

    def generate_invoice():
        pass
