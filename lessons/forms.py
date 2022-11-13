from django import forms
from.models import Request

class RequestForm(forms.ModelForm):

    class Meta:
        model = Request
        exclude = ['status']
    
    
class SignUpForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=50)
    last_name = forms.CharField(label='Last name', max_length=50)
    email = forms.CharField(label='Email', max_length=50)
    new_password = forms.CharField(label='password', widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())
    
