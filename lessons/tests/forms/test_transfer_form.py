from lessons.models import User
from django.test import TestCase
from lessons.forms import TransferForm
from django import forms

class TransferFormTestCase(TestCase):
    fixtures = ['lessons/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.form_input = {'amount': 8.12}
        
    def test_form_contains_required_fields(self):
        form = TransferForm()
        self.assertIn('amount', form.fields)
        amount = form.fields['amount']
        self.assertTrue(isinstance(amount, forms.DecimalField))

    def test_form_accepts_valid_input(self):
        form = TransferForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_input(self):
        self.form_input['amount'] = ''
        form = TransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_invalid_number(self):
        self.form_input['amount'] = 9.999
        form = TransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())