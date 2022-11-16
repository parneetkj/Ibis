from django import forms
from django.test import TestCase
from ..forms import RequestForm
from ..models import Request
import datetime

class SignUpFormTestCase(TestCase):
    """Unit tests of the sign up form."""

    def setUp(self):
        self.form_input = {
            'student': 'Jake',
            'date' : '2022-12-12',
            'time' : '20:20',
            'amount' : 4,
            'interval': 1,
            'duration': 30,
            'topic': 'Violin',
            'teacher': 'Mrs.Smith'
        }

    def test_valid_request_form(self):
        form = RequestForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = RequestForm()
        self.assertIn('student', form.fields)
        self.assertIn('date', form.fields)
        date = form.fields['date']
        self.assertTrue(isinstance(date, forms.DateField))
        self.assertIn('time', form.fields)
        time = form.fields['time']
        self.assertTrue(isinstance(time, forms.TimeField))
        self.assertIn('amount', form.fields)
        amount = form.fields['amount']
        self.assertTrue(isinstance(amount, forms.IntegerField))
        self.assertIn('interval', form.fields)
        interval = form.fields['interval']
        self.assertTrue(isinstance(interval, forms.IntegerField))
        self.assertIn('duration', form.fields)
        duration = form.fields['duration']
        self.assertTrue(isinstance(duration, forms.ChoiceField))
        self.assertIn('topic', form.fields)
        self.assertIn('teacher', form.fields)
    
    def test_form_does_not_have_status_field(self):
        form = RequestForm()
        self.assertNotIn('status', form.fields)

    def test_form_uses_model_validation(self):
        self.form_input['duration'] = 61
        form = RequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_date_should_not_be_in_the_past(self):
        self.form_input['date'] = "2022-11-16"
        form = RequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = RequestForm(data=self.form_input)
        before_count = Request.objects.count()
        form.save()
        after_count = Request.objects.count()
        self.assertEqual(after_count, before_count+1)
        request = Request.objects.get(student="Jake")
        self.assertEqual(request.date, datetime.date(2022,12,12))
        self.assertEqual(request.time, datetime.time(20,20))
        self.assertEqual(request.interval, 1)
        self.assertEqual(request.duration, 30)
        self.assertEqual(request.topic, 'Violin')
        self.assertEqual(request.teacher, 'Mrs.Smith')
        self.assertEqual(request.status, 'In Progress')