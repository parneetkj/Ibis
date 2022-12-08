from django import forms
from django.test import TestCase
from ...forms import BookingForm
from ...models import Booking, User
import datetime

class BookingTestCase(TestCase):
    """Unit tests of the booking form."""

    fixtures = ['lessons/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')

        self.form_input = {
            'day':'Monday',
            'time':'14:30',
            'start_date':'2022-11-16',
            'duration':30,
            'interval':1,
            'teacher':'Mrs.Smith',
            'no_of_lessons':4,
            'topic':'Violin',
        }

    def test_valid_request_form(self):
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = BookingForm()
        self.assertIn('day', form.fields)
        self.assertIn('time', form.fields)
        self.assertIn('start_date', form.fields)
        self.assertIn('duration', form.fields)
        duration = form.fields['duration']
        self.assertTrue(isinstance(duration, forms.ChoiceField))
        self.assertIn('interval', form.fields)
        interval = form.fields['interval']
        self.assertTrue(isinstance(interval, forms.IntegerField))
        self.assertIn('teacher', form.fields)
        self.assertIn('no_of_lessons', form.fields)
        no_of_lessons = form.fields['no_of_lessons']
        self.assertTrue(isinstance(no_of_lessons, forms.IntegerField))
        self.assertIn('topic', form.fields)

    def test_form_does_not_have_student_field(self):
        form = BookingForm()
        self.assertNotIn('student', form.fields)

    def test_form_does_not_have_student_field(self):
        form = BookingForm()
        self.assertNotIn('student', form.fields)

    def test_form_uses_model_validation(self):
        self.form_input['duration'] = 61
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
