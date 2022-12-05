"""Test case of edit booking view"""

from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Booking
from lessons.forms import BookingForm
from lessons.tests.helpers import create_bookings

class UpdateBookingViewTestCase(TestCase):
    """Test case of edit booking view"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json',
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')

        self.data = {
            'day':'Monday',
            'time':'14:30',
            'start_date':'2022-11-16',
            'duration':30,
            'interval':1,
            'teacher':'Mrs.Smith',
            'no_of_lessons':4,
            'topic':'Update__Test',
            'cost': '14.50'
        }
        create_bookings(self.user, 1, 3)
        self.bookings = Booking.objects.filter(student = self.user)

    def test_update_booking_displays_correct_page(self):
        self.client.login(username=self.admin.username, password='Password123')
        booking_url = reverse('update_booking', kwargs={'id': self.bookings[0].pk})
        response = self.client.get(booking_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_booking.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BookingForm))
        self.assertContains(response, "Topic__1")

    def test_redirect_with_incorrect_booking_id(self):
        self.client.login(username=self.admin.username, password='Password123')
        booking_url = reverse('update_booking', kwargs={'id': (Booking.objects.count()) +1})
        redirect_url = reverse('bookings')
        response = self.client.get(booking_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'bookings.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_update_booking_correctly_saves(self):
        self.client.login(username=self.admin.username, password='Password123')
        booking_url = reverse('update_booking', kwargs={'id': self.bookings[0].pk})
        response = self.client.get(booking_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_booking.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BookingForm))
        self.assertContains(response, "Topic__1")

        before_count = Booking.objects.count()
        update_response = self.client.post(booking_url, self.data, follow=True)
        after_count = Booking.objects.count()
        self.assertEqual(before_count, after_count)

        self.assertEqual(update_response.status_code, 200)
        self.assertTemplateUsed(update_response, 'bookings.html')
        messages_list = list(update_response.context['messages'])
        self.assertEqual(len(messages_list), 1)

        self.assertEqual(self.bookings[0].topic, 'Update__Test')

    def test_update_does_not_save_if_form_is_invalid(self):
        self.client.login(username=self.admin.username, password='Password123')
        booking_url = reverse('update_booking', kwargs={'id': self.bookings[0].pk})
        response = self.client.get(booking_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_booking.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BookingForm))
        self.assertContains(response, "Topic__1")

        self.data['interval'] =' 1000'

        before_count = Booking.objects.count()
        update_response = self.client.post(booking_url, self.data, follow=True)
        after_count = Booking.objects.count()
        self.assertEqual(before_count, after_count)

        self.assertEqual(update_response.status_code, 200)
        self.assertTemplateUsed(update_response, 'update_booking.html')
        self.assertEqual(self.bookings[0].interval, 1)

    def test_students_cannot_access_update_bookings_page(self):
        self.client.login(username=self.user.username, password='Password123')
        booking_url = reverse('update_booking', kwargs={'id': self.bookings[0].pk})
        redirect_url = reverse('feed')
        response = self.client.get(booking_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
