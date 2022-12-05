"""Test case of new request view"""

from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Request
from lessons.forms import RequestForm
from lessons.tests.helpers import create_requests,reverse_with_next

class NewRequestViewTestCase(TestCase):
    """Test case of new request view"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json',
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')

        self.data = {
            'date':'2023-12-12',
            'time':'14:30',
            'amount':4,
            'interval':1,
            'duration':30,
            'topic':'violin',
            'teacher':'Mrs.Smith'
        }
        
        self.url = reverse('new_request')

    def test_new_request_url(self):
        self.assertEqual(self.url,f'/new_request/')

    def test_get_new_request(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_request.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RequestForm))
        self.assertFalse(form.is_bound)

    def test_get_new_request_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_new_request_redirects_when_is_admin(self):
        self.client.login(username=self.admin.username, password='Password123')
        redirect_url = reverse('feed')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_successful_new_request(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = Request.objects.count()
        response = self.client.post(self.url, self.data, follow=True)
        after_count = Request.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pending_requests.html')

    def test_unsuccessful_new_request(self):
        self.client.login(username=self.user.username, password="Password123")
        count_before = Request.objects.count()
        self.data['time'] = "not a time"
        response = self.client.post(self.url, self.data)
        count_after = Request.objects.count()
        self.assertEqual(count_after, count_before)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_request.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RequestForm))
        self.assertTrue(form.is_bound)