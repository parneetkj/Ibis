from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.forms import CreateAdminForm
from lessons.tests.helpers import reverse_with_next
from django.contrib.auth.hashers import check_password

class TestNewAdminViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_director.json',
        'lessons/tests/fixtures/default_admin.json',
    ]
    def setUp(self):
        self.url = reverse('create_admin')
        self.user = User.objects.get(username='bobdoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')
        self.form_input = {
            'first_name': 'Peter',
            'last_name': 'Doe',
            'username': 'peterdoe@example.org',
            'is_director': True,
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }

    def test_create_admin_url(self):
        self.assertEqual(self.url,'/create_admin')

    def test_get_create_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_admin.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateAdminForm))
        self.assertFalse(form.is_bound)

    def test_get_create_admin_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


    def test_unsuccessful_creation_of_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_admin.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateAdminForm))
        self.assertTrue(form.is_bound)


    def test_successful_creation_of_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(before_count + 1, after_count)
        response_url = reverse('manage_admin')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'manage_admin.html')
        user = User.objects.get(username='peterdoe@example.org')
        self.assertEqual(user.first_name, 'Peter')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.is_director, True)
        self.assertEqual(user.is_admin, True)
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)

    def test_post_create_admin_redirects_when_admin_created(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(before_count + 1, after_count)
        redirect_url = reverse('manage_admin')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'manage_admin.html')
