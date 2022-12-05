from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Booking
from lessons.tests.helpers import reverse_with_next

class DeleteBookingViewTestCase(TestCase):
    """Test case of delete booking view"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json',
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')
    
        self.bookingData = Booking(
            student=self.user,
            day = 'Mon',
            start_date = '2023-12-12',
            time = '20:20',
            no_of_lessons=4,
            interval=1,
            duration=30,
            teacher='Mrs.Smith', 
            topic = "Violin",
            cost=14.50
        )
        self.bookingData.save()
        self.bookingData.generate_invoice()
        self.bookings = Booking.objects.filter(student = self.user)

        self.url = reverse('delete_booking', kwargs={'id': self.bookings[0].pk})

    def test_get_delete_booking_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_delete_booking_redirects_admin_correctly(self):
        self.client.login(username=self.admin.username, password='Password123')
        redirect_url = reverse('bookings')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'bookings.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_students_cannot_access_delete_bookings_page(self):
        self.client.login(username=self.user.username, password='Password123')
        redirect_url = reverse('feed')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_delete_booking_deletes_correct_booking(self):
        self.client.login(username=self.admin.username, password='Password123')
        before_count = Booking.objects.count()
        pk = self.bookings[0].pk
        booking_url = reverse('delete_booking', kwargs={'id': pk})
        redirect_url = reverse('bookings')
        response = self.client.get(booking_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        after_count = Booking.objects.count()
        self.assertEqual(before_count - 1, after_count)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_delete_booking_redirects_if_not_found(self):
        self.client.login(username=self.admin.username, password='Password123')
        booking_url = reverse('delete_booking', kwargs={'id': (Booking.objects.count()) +1})
        redirect_url = reverse('bookings')
        response = self.client.get(booking_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'bookings.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)