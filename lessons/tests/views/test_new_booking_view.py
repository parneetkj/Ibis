from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Request, Booking
from lessons.forms import BookingForm
from lessons.tests.helpers import create_requests,reverse_with_next

class NewBookingViewTestCase(TestCase):
    """Test case of new booking view"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json',
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')

        create_requests(self.user, 0, 5)
        self.requests = Request.objects.filter()

        self.data = {
            'day':'Monday',
            'time':'14:30',
            'start_date':'2022-11-16',
            'duration':30,
            'interval':1,
            'teacher':'Mrs.Smith',
            'no_of_lessons':4,
            'topic':'violin',
            'cost': 14.50
        }
        
        self.bookings = Booking.objects.filter()
        self.url = reverse('new_booking', kwargs={'id': self.requests[0].pk})

    def test_new_booking_url(self):
        self.assertEqual(self.url,f'/new_booking/{self.requests[0].pk}')

    def test_get_new_booking(self):
        self.client.login(username=self.admin.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_booking.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BookingForm))
        self.assertFalse(form.is_bound)

    def test_get_new_booking_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_new_booking_redirects_when_is_student(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('new_booking', kwargs={'id': self.requests[0].pk})
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_successful_new_booking(self):
        self.client.login(username=self.admin.username, password="Password123")
        before_count = Booking.objects.count()
        response = self.client.post(self.url, self.data, follow=True)
        after_count = Booking.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccessful_new_booking(self):
        self.client.login(username=self.admin.username, password="Password123")
        count_before = Booking.objects.count()
        self.data['teacher'] = ""
        response = self.client.post(self.url, self.data)
        count_after = Booking.objects.count()
        self.assertEqual(count_after, count_before)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_booking.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BookingForm))

    def test_new_booking_displays_request_information_belonging_to_the_chosen_user_only(self):
        self.client.login(username=self.user.username, password='Password123')
        other_user = User.objects.get(username='janedoe@example.org')
        create_requests(other_user, 100, 100)
        create_requests(self.user, 200, 200)
        url = reverse('new_booking', kwargs={'id': 200})
        response = self.client.get(url)
        for count in range(200, 200):
            self.assertContains(response, f'Topic__{count}')
        for count in range(300, 300):
            self.assertNotContains(response, f'Topic__{count}')

    def test_redirect_with_incorrect_request_id(self):
        self.client.login(username=self.admin.username, password='Password123')
        url = reverse('new_booking', kwargs={'id': (Request.objects.count()) +100})
        redirect_url = reverse('feed')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)