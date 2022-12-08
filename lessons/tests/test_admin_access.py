from django.test import TestCase, RequestFactory
from lessons.models import User, Request, Booking
from lessons.views import feed, home_page, SignUpView, LogInView, update_request, new_request,delete_request, manage_admin, create_admin, delete_admin, promote_admin, update_admin
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from lessons.forms import LogInForm, RequestForm

"""
Tests to see if an admin cannot access the views they shouldn't be allowed to
Some tests for views that admins can access are omitted as they are already tested in their respective test views
"""

class AdminPermissionTestCase(TestCase):
    fixtures = ['lessons/tests/fixtures/default_admin.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(username='petra.pickles@example.org')
        self.adminList = User.objects.filter(is_admin=True)

    def test_admin_access_feed_page(self):
        request = self.factory.get('/feed')
        request.user = self.user
        response = feed(request)
        self.assertEqual(response.status_code, 200)

    def test_admin_access_home_page(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home_page(request)
        self.assertEqual(response.status_code, 200)

    def test_admin_access_log_in(self):
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('log_in')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_is_admin_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        self.assertFalse(self.user.is_student, False)
        self.assertTrue(self.user.is_admin, True)
        self.assertFalse(self.user.is_director, False)

    def test_admin_access_sign_up(self):
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('sign_up')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_admin_access_update_request(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('update_request', kwargs={'id': (self.adminList[0].pk)})
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_admin_access_new_request(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('new_request')
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_admin_access_delete_request(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('delete_request', kwargs={'id': (self.adminList[0].pk)})
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_admin_access_manage_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('manage_admin')
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_admin_access_update_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('update_admin', kwargs={'pk': (self.adminList[0].pk)})
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_admin_access_create_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('create_admin')
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_admin_access_delete_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('delete_admin', kwargs={'name': (self.user.username)})
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_admin_access_promote_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('promote_admin', kwargs={'pk': (self.adminList[0].pk)})
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
