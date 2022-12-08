from django.test import TestCase, RequestFactory
from lessons.models import User, Booking
from lessons.views import feed, home_page, SignUpView, LogInView, manage_admin, delete_booking, update_booking, new_booking, manage_admin, create_admin, delete_admin, transfers
from django.urls import reverse
from lessons.forms import LogInForm, BookingForm
from lessons.tests.helpers import create_bookings

"""
Tests to see if a student cannot access the views they shouldn't be allowed to
Some tests for views that students can access are omitted as they are already tested in their respective test views
"""

class StudentPermissionTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json'
        ]
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(username='johndoe@example.org')
        self.studentList = User.objects.filter(is_student=True)
        self.data = {
            'day':'Monday',
            'time':'14:30',
            'start_date':'2022-11-16',
            'duration':30,
            'interval':1,
            'teacher':'Mrs.Smith',
            'no_of_lessons':4,
            'topic':'Update__Test',
            'cost': 14.50

        }
        create_bookings(self.user, 1, 3)
        self.bookings = Booking.objects.filter(student = self.user)


    def test_student_access_home_page(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home_page(request)
        self.assertEqual(response.status_code, 200)

    def test_student_access_log_in(self):
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('log_in')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_is_student_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        self.assertTrue(self.user.is_student, True)
        self.assertFalse(self.user.is_admin, False)
        self.assertFalse(self.user.is_director, False)

    def test_student_access_sign_up(self):
        self.url = reverse('sign_up')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')

    def test_student_access_feed_page(self):
        request = self.factory.get('/feed')
        request.user = self.user
        response = feed(request)
        self.assertEqual(response.status_code, 200)

    def test_student_access_update_booking(self):
        self.client.login(username=self.user.username, password='Password123')
        booking_url = reverse('update_booking', kwargs={'id': (Booking.objects.count())})
        redirect_url = reverse('feed')
        response = self.client.get(booking_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_student_access_new_booking(self):
        self.client.login(username=self.user.username, password='Password123')
        booking_url = reverse('new_booking', kwargs={'id': (Booking.objects.count())})
        redirect_url = reverse('feed')
        response = self.client.get(booking_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_student_access_delete_booking(self):
        self.client.login(username=self.user.username, password='Password123')
        booking_url = reverse('delete_booking', kwargs={'id': (Booking.objects.count())})
        redirect_url = reverse('feed')
        response = self.client.get(booking_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_student_access_manage_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('manage_admin')
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_student_access_update_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('update_admin', kwargs={'pk': (self.studentList[0].pk)})
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_student_access_create_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('create_admin')
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_student_access_delete_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('delete_admin', kwargs={'name': (self.user.username)})
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_student_access_promote_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('promote_admin', kwargs={'pk': (self.studentList[0].pk)})
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
