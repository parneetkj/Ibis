from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from lessons.forms import UpdateAdminForm
from lessons.models import User
from django.urls import reverse

class UpdateAdminFormTestCase(TestCase):
    fixtures = ['lessons/tests/fixtures/default_admin.json',
                'lessons/tests/fixtures/default_director.json']

    def setUp(self):
        self.user = User.objects.get(username='bobdoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')
        self.form_input = {
            'first_name': 'Petra',
            'last_name': 'Pickles',
            'username': 'petra.pickles@example.org',
            'password': 'Password123',
            'password_confirmation': 'Password123'

        }

    def test_valid_sign_up_form(self):
        self.client.login(username=self.user.username, password='Password123')
        form = UpdateAdminForm(instance=self.admin, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = UpdateAdminForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        self.assertIn('password_confirmation', form.fields)

    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'badusername'
        form = UpdateAdminForm(instance=self.admin, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = UpdateAdminForm(instance=self.admin, data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        user = User.objects.get(username='petra.pickles@example.org')
        self.assertEqual(user.first_name, 'Petra')
        self.assertEqual(user.last_name, 'Pickles')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
