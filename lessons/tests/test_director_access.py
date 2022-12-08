from django.test import TestCase, RequestFactory
from lessons.models import User, Request, Booking
from lessons.views import feed, home_page, SignUpView, LogInView, update_request, new_request,delete_request, manage_admin, create_admin, delete_admin
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from lessons.forms import LogInForm, RequestForm

"""
Tests to see if a director cannot access the views they shouldn't be allowed to
Some tests for views that directors can access are omitted as they are already tested in their respective test views
"""

class DirectorPermissionTestCase(TestCase):
    fixtures = ['lessons/tests/fixtures/default_director.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(username='bobdoe@example.org')
        self.directorList = User.objects.filter(is_director=True)

    def test_director_access_feed_page(self):
        request = self.factory.get('/feed')
        request.user = self.user
        response = feed(request)
        self.assertEqual(response.status_code, 200)

    def test_director_access_home_page(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home_page(request)
        self.assertEqual(response.status_code, 200)

    def test_director_access_log_in(self):
        self.url = reverse('log_in')
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow = True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_is_director_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        self.assertFalse(self.user.is_student, False)
        self.assertTrue(self.user.is_admin, True)
        self.assertTrue(self.user.is_director, True)

    def test_director_access_sign_up(self):
        self.url = reverse('sign_up')
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow = True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_director_access_new_request(self):
        self.url = reverse('new_request')
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow = True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_director_access_update_request(self):
        self.url = reverse('update_request', kwargs={'id': self.directorList[0].pk})
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow = True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_director_access_delete_request(self):
        self.url = reverse('delete_request', kwargs={'id': self.directorList[0].pk})
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow = True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_director_access_pay_invoice(self):
        self.url = reverse('pay_invoice', kwargs={'booking_id': self.directorList[0].pk})
        self.client.login(username=self.user.username, password='Password123')
        redirect_url = reverse('feed')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
