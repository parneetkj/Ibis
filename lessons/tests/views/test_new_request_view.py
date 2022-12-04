from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Request
from lessons.forms import RequestForm
from lessons.tests.helpers import create_requests,reverse_with_next
import datetime

class NewRequestTestCase(TestCase):
    """Tests of the new request view."""

    fixtures = ['lessons/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('new_request')
        self.user = User.objects.get(username='johndoe@example.org')
        self.form_input = {
            'date': '2023-12-12',
            'time': '20:20',
            'amount': 4,
            'interval':'1',
            'duration': '30',
            'topic':'Violin',
            'teacher':'Mrs.Smith'
        }

    def test_new_request_saves_correctly(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = Request.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Request.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RequestForm))
        self.assertFalse(form.is_bound)

        request = Request.objects.get(student=self.user)
        self.assertEqual(request.date, datetime.date(2023, 12, 12))
        self.assertEqual(request.time, datetime.time(20,20))
        self.assertEqual(request.amount, 4)
        self.assertEqual(request.interval, 1)
        self.assertEqual(request.duration, 30)
        self.assertEqual(request.topic, 'Violin')
        self.assertEqual(request.teacher, 'Mrs.Smith')

    def test_incorrect_request_is_rejected(self):
        self.form_input['amount'] = 1000
        self.client.login(username=self.user.username, password='Password123')
        before_count = Request.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Request.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RequestForm))
        self.assertTrue(form.is_bound)

    def test_new_request_redirects_if_not_logged_in(self):
        before_count = Request.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Request.objects.count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')
    
    def test_new_request_get_request_is_forbidden(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 403)