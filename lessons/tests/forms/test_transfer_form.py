from django import forms
from django.test import TestCase
from lessons.forms import TransferForm

class TransferFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {'amount_paid': 8.12}

    def test_form_contains_required_fields(self):
        form = TransferForm()
        self.assertIn('amount_paid', form.fields)

    def test_form_accepts_valid_input(self):
        form = TransferForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_input(self):
        self.form_input['amount_paid'] = ''
        form = TransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_invalid_number(self):
        self.form_input['amount_paid'] = 9.999
        form = TransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())