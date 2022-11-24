"""Test case of pending requests view"""

from django.test import TestCase
from django.urls import reverse
from lessons.forms import RequestForm
from lessons.models import User
from lessons.tests.helpers import reverse_with_next

class PendingRequestsViewTestCase(TestCase):
    """Test case of pending requests view"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.url = reverse('pending_requests')
        self.user = User.objects.get(username='@johndoe')
    
    def test_pending_requests_url(self):
        self.assertEqual(self.url,'/pending_requests/')
    
    def test_get_pending_requests(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pending_requests.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RequestForm))
        self.assertFalse(form.is_bound)

    def test_get_pending_request_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
