"""Test case of edit booking view"""

from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Booking
from lessons.forms import BookingForm
from lessons.tests.helpers import reverse_with_next, create_requests

class UpdateBookingViewTestCase(TestCase):
    """Test case of edit booking view"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.bookingData = Booking(
            student=self.user,
            day = 'Mon',
            start_date = '2023-12-12',
            time = '20:20',
            no_of_lessons=4,
            interval=1,
            duration=30,
            teacher='Mrs.Smith'
        )
        self.bookingData.save()
        self.bookings = Booking.objects.filter(student = self.user)

    def test_update_booking_displays_correct_page(self):
        self.client.login(username=self.user.username, password='Password123')
        booking_url = reverse('update_booking', kwargs={'id': self.bookings[0].pk})
        response = self.client.get(booking_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_booking.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BookingForm))
        self.assertContains(response, "Mrs.Smith")

    def test_redirect_with_incorrect_booking_id(self):
        self.client.login(username=self.user.username, password='Password123')
        booking_url = reverse('update_booking', kwargs={'id': (Booking.objects.count()) +1})
        redirect_url = reverse('bookings')
        response = self.client.get(booking_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'bookings.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 2)
    
    def test_update_correctly_saves(self):
        self.client.login(username=self.user.username, password='Password123')
        booking_url = reverse('update_booking', kwargs={'id': self.bookings[0].pk})
        response = self.client.get(booking_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_booking.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BookingForm))
        self.assertContains(response, "Mrs.Smith")

        #Change a value in the form
        #Check against the database