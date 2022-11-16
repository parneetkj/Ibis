from django import forms
from django.core.exceptions import ValidationError
from.models import Request
import datetime

class RequestForm(forms.ModelForm):

    class Meta:
        model = Request
        exclude = ['status']

    def clean(self):
        super().clean()
        date = self.cleaned_data.get('date')
        if date <= datetime.date.today():
            self.add_error('date','Date must be in the future.')