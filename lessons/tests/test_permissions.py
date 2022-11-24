from django.contrib.auth.models import User
from django.test import TestCase

class AnonymousUserTestCase(TestCase):

    def access_feed_page(self):
        response = self.client.get('/feed/')
        self.assertRedirects(response, '/login/')



class StudentPermissionTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.org',
            'password': 'Password123',
        }
        self.is_student = True
        self.user.save()

class AdminPermissionTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.org',
            'password': 'Password123',
        }
        self.is_admin = True
        self.user.save()

    def test_access_feed_page(self):
        reponse = self.client.get(url)
        self.client.login(first_name = 'Jane', last_name = 'Doe', email
        = 'janedoe@example.org', password = 'password')
        self.assertRedirects('/login/')
