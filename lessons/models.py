from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator

# Create your models here.
class Request(models.Model):
    """Requests by students"""

    student = models.CharField(max_length=50, blank=False)
    availability = models.CharField(max_length=200, blank=False)
    amount = models.IntegerField(
        validators=[
            MinLengthValidator(
                limit_value=1,
                message="Must book at least 1 lesson."
            ),
            MaxLengthValidator(
                limit_value=50,
                message="Cannot book more than 50 lessons."
            )
        ]
    )
    interval = models.IntegerField(
        validators=[
            MinLengthValidator(
                limit_value=1,
                message="Must book at least 1 week of lessons."
            ),
            MaxLengthValidator(
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
        default="Any"
    )
    teacher = models.CharField(
        max_length=100,
        default="Any"
    )
    
