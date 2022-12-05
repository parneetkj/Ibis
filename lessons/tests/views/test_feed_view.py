"""Test case of feed view"""

from django.test import TestCase
from django.urls import reverse
from lessons.forms import RequestForm
from lessons.models import User
from lessons.tests.helpers import reverse_with_next, create_requests

class FeedViewTestCase(TestCase):
    """Test case of feed view"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.url = reverse('feed')
        self.user = User.objects.get(username='johndoe@example.org')
    
    def test_feed_url(self):
        self.assertEqual(self.url,'/feed/')
    
    def test_get_feed(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_get_show_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)