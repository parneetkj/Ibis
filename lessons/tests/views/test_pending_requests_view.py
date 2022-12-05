"""Test case of pending requests view"""

from django.test import TestCase
from django.urls import reverse
from lessons.forms import RequestForm
from lessons.models import User, Request
from lessons.tests.helpers import reverse_with_next, create_requests

class PendingRequestsViewTestCase(TestCase):
    """Test case of pending requests view"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json',
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.url = reverse('pending_requests')
        self.user = User.objects.get(username='johndoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')
        create_requests(self.user,0,5)
        self.requests = Request.objects.filter()

    def test_pending_requests_url(self):
        self.assertEqual(self.url,'/pending_requests/')
    
    def test_get_pending_requests(self):
        self.client.login(username=self.admin.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pending_requests.html')
    
    def test_pending_requests_shows_student_only_their_requests(self):
        self.client.login(username=self.user.username, password='Password123')
        other_user = User.objects.get(username='janedoe@example.org')
        create_requests(other_user, 10, 20)
        create_requests(self.user, 30, 40)
        response = self.client.get(self.url)
        for count in range (10,20):
            self.assertNotContains(response, f'Topic__{count}')
        for count in range (30,40):
            self.assertContains(response, f'Topic__{count}')

    def test_pending_requests_shows_admin_all_requests(self):
        self.client.login(username=self.admin.username, password='Password123')
        other_user = User.objects.get(username='janedoe@example.org')
        create_requests(other_user, 10, 20)
        create_requests(self.user, 30, 40)
        response = self.client.get(self.url)
        for count in range (10,20):
            self.assertContains(response, f'Topic__{count}')
        for count in range (30,40):
            self.assertContains(response, f'Topic__{count}')

    def test_get_pending_request_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
