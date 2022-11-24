from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Request, Booking
from lessons.forms import BookingForm
from lessons.tests.helpers import create_requests

class NewBookingViewTestCase(TestCase):
    """Test case of new booking view"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.requestData = Request(
            student=self.user,
            date = '2023-12-12',
            time = '20:20',
            amount=4,
            interval=1,
            duration=30,
            topic="Violin",
            teacher='Mrs.Smith'
        )
        self.requestData.save()
        self.target_request = Request.objects.get(student = self.user)
        self.url = reverse('new_booking', kwargs={'request_id': self.target_request.id})

    def test_new_booking_url(self):
        self.assertEqual(self.url,f'/new_booking/{self.target_request.id}')

    def test_get_new_booking(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_booking.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BookingForm))
        self.assertContains(response, "Mrs.Smith")

    #Add tests for when POST request is used

    def test_redirect_with_incorrect_request_id(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('new_booking', kwargs={'request_id': (Request.objects.count()) +1})
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
    
    def test_booking_correctly_saves(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_booking.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BookingForm))
        self.assertContains(response, "Mrs.Smith")

    def test_new_booking_displays_request_information_belonging_to_the_chosen_user_only(self):
        self.client.login(username=self.user.username, password='Password123')
        other_user = User.objects.get(username='@janedoe')
        create_requests(other_user, 100, 100)
        create_requests(self.user, 200, 200)
        url = reverse('new_booking', kwargs={'request_id': 200})
        response = self.client.get(url)
        for count in range(200, 200):
            self.assertContains(response, f'Topic__{count}')
        for count in range(300, 300):
            self.assertNotContains(response, f'Topic__{count}')