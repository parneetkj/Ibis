from django import forms
from .models import User, Request, Booking, Term
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        exclude = ['student','status']

    """Override clean method to check date and time"""
    def clean(self):
        super().clean()
        date = self.cleaned_data.get('date')
        if (date == None):
            return
        if(date <= timezone.now().date()):
            self.add_error('date','Date must be in the future.')
            time = self.cleaned_data.get('time')
            if (time == None):
                return
            if (date == timezone.now().date() and time <= timezone.now().time()):
                self.add_error('time','Time must be in the future.')


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking    
        exclude = ['student', 'no_of_lessons']

    def clean(self):
        super().clean()
        term = self.cleaned_data.get('term')
        if (term == None):
            return
        if(term.end_date <= timezone.now().date()):
            self.add_error('term','Term must be in the future.')


class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
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

class TermForm(forms.ModelForm):
    """Form enabling admin users to create Terms."""

    class Meta:
        """Form options."""

        model = Term
        fields = ['start_date', 'end_date']

    """Override clean method to check for overlapping terms"""
    def clean(self):
        super().clean()

        start_date=self.cleaned_data.get('start_date')
        end_date=self.cleaned_data.get('end_date')

        terms = Term.objects.filter()

        overlap = False
        if (start_date == None) or (end_date ==None): 
            return
        elif (end_date <= start_date):
            self.add_error('start_date','Term entered is invalid')
            self.add_error('end_date','Term entered is invalid')
        else:
            for term in terms:
                other_start_date = term.start_date
                other_end_date = term.end_date
                if (start_date <= other_end_date) and (other_start_date <= end_date):
                    overlap = True

            if overlap:
                self.add_error('start_date','Term entered overlaps with an existing term.')
                self.add_error('end_date','Term entered overlaps with an existing term.')