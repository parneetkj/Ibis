from django import forms
from.models import Request
from.models import User


class RequestForm(forms.ModelForm):

    class Meta:
        model = Request
        exclude = ['status']
    
    
class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']
   
    new_password = forms.CharField(label='password', widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())
    
