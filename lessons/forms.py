from django import forms
from .models import User, Request, Booking
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django.db import models
from django.contrib.auth.forms import UserChangeForm

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        exclude = ['student','status']
        localized_fields = ('date','time')
        labels = {
            'date': ('Date (YYYY-MM-DD)'),
            'time': ('Time (HH:MM)'),
            'amount': ('Number of lessons:'),
            'interval': ('Number of weeks between lessons'),
        }


    """Override clean method to check date and time"""
    def clean(self):
        super().clean()
        date = self.cleaned_data.get('date')
        if (date == None):
            self.add_error('date','Please enter the date as YYYY-MM-DD.')
            return

        time = self.cleaned_data.get('time')
        if (time == None):
            self.add_error('time','Please enter the time as HH:MM.')
            return

        if(date <= timezone.now().date()):
            self.add_error('date','Date must be in the future.')
            if (date == timezone.now().date() and time <= timezone.now().time()):
                self.add_error('time','Time must be in the future.')

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['student']

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user

class SignUpForm(forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'username': 'Email',
        }


    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            password=self.cleaned_data.get('new_password'),
            is_student = True,


        )
        return user

class TransferForm(forms.Form):
    amount = forms.DecimalField(
        label='Amount Paid:',
        min_value=0,
        step_size=0.01,
        decimal_places=2,
        max_digits=10
        )

class SelectStudentForm(forms.Form):
    student = forms.ModelChoiceField(queryset=User.objects.filter(is_student=True))

class CreateAdminForm(forms.ModelForm):
    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'username': 'Email',
        }

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            password=self.cleaned_data.get('new_password'),
            is_admin = True,

        )
        return user


class UpdateAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = {
            'username': 'Email',
        }

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def __init__(self, *args, **kwargs):
        super(UpdateAdminForm, self).__init__(*args, **kwargs)

        for username, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
