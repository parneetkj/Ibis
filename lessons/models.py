from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
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
    balance = models.FloatField(default=0)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def increase_balance(self,amount):
        self.balance += amount
        return self.balance

    def decrease_balance(self,amount):
        self.balance -= amount
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

class Term(models.Model):
    """ Term model for music school """

    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
        
def get_default_term():
    terms = Term.objects.all().order_by('start_date')
    default_term = None
    count = 0
    while not default_term: 
        term = terms[count]

        if (term.end_date > timezone.now().date()) and (term.start_date < timezone.now().date()) :
            default_term = term
        elif (term.start_date > timezone.now().date()):
            default_term = term

        count += 1

    return default_term

class Booking(models.Model):
    """ Booking by admin """

    student = models.ForeignKey(User, on_delete=models.CASCADE)

    term = models.ForeignKey(Term, on_delete=models.CASCADE, default=get_default_term)
    
    start_date = models.DateField(blank=False)

    end_date = models.DateField(blank=False)

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
    
    topic = models.CharField(
        max_length=50,
        blank=False
    )

    no_of_lessons = models.IntegerField(default=0)

    

    def generate_invoice():
        pass

    def calc_no_of_lessons(self):
        duration = self.end_date - self.start_date
        duration_in_weeks = duration.days / 7
        self.no_of_lessons = duration_in_weeks // self.interval
        self.save()
