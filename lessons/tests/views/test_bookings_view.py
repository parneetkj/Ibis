"""Test case of bookings view"""

from django.test import TestCase
from django.urls import reverse
from lessons.forms import BookingForm
from lessons.models import User
from lessons.tests.helpers import create_bookings, reverse_with_next

class BookingsViewTestCase(TestCase):
    """Test case of bookings view"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json',
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.url = reverse('bookings')
        self.user = User.objects.get(username='johndoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')
    
    def test_bookings_url(self):
        self.assertEqual(self.url,'/bookings/')
    
    def test_get_bookings(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings.html')
    
    def test_booking_displays_bookings_of_the_user_only(self):
        self.client.login(username=self.user.username, password='Password123')
        other_user = User.objects.get(username='janedoe@example.org')
        create_bookings(other_user, 10, 20)
        create_bookings(self.user, 30, 40)
        response = self.client.get(self.url)
        for count in range (10,20):
            self.assertNotContains(response, f'Topic__{count}')
        for count in range (30,40):
            self.assertContains(response, f'Topic__{count}')

    def test_booking_displays_all_bookings_for_the_admins(self):
        self.client.login(username=self.admin.username, password='Password123')
        other_user = User.objects.get(username='janedoe@example.org')
        create_bookings(other_user, 10, 20)
        create_bookings(self.user, 30, 40)
        response = self.client.get(self.url)
        for count in range (10,20):
            self.assertContains(response, f'Topic__{count}')
        for count in range (30,40):
            self.assertContains(response, f'Topic__{count}')

    def test_get_bookings_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)