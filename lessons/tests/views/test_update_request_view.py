from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Request
from lessons.forms import RequestForm
from lessons.tests.helpers import reverse_with_next, create_requests

class UpdateRequestViewTestCase(TestCase):
    """Test case of edit request view"""
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.form_input = {
            'date': '2023-12-12',
            'time': '20:20',
            'amount': 4,
            'interval':'1',
            'duration': '30',
            'topic':'Update__Test',
            'teacher':'Mrs.Smith'
        }
        create_requests(self.user,1,3)
        self.requests = Request.objects.filter(student = self.user)

    def test_update_request_displays_correct_page(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('update_request', kwargs={'id': self.requests[0].pk})
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_request.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RequestForm))
        self.assertContains(response, "Topic__1")

    def test_redirect_with_incorrect_request_id(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('update_request', kwargs={'id': (Request.objects.count()) +1})
        redirect_url = reverse('feed')
        response = self.client.get(request_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_update_correctly_saves(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('update_request', kwargs={'id': self.requests[0].pk})
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_request.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RequestForm))
        self.assertContains(response, "Topic__1")

        before_count = Request.objects.count()
        update_response = self.client.post(request_url, self.form_input, follow=True)
        after_count = Request.objects.count()
        self.assertEqual(before_count, after_count)

        self.assertEqual(update_response.status_code, 200)
        self.assertTemplateUsed(update_response, 'feed.html')
        messages_list = list(update_response.context['messages'])
        self.assertEqual(len(messages_list), 1)

        self.requests = Request.objects.filter(student = self.user)
        self.assertEqual(self.requests[0].topic, 'Update__Test')

    def test_update_does_not_save_if_form_is_invalid(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('update_request', kwargs={'id': self.requests[0].pk})
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_request.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RequestForm))
        self.assertContains(response, "Topic__1")

        self.form_input['interval'] =' 1000'

        before_count = Request.objects.count()
        update_response = self.client.post(request_url, self.form_input, follow=True)
        after_count = Request.objects.count()
        self.assertEqual(before_count, after_count)

        self.assertEqual(update_response.status_code, 200)
        self.assertTemplateUsed(update_response, 'update_request.html')
        
        self.requests = Request.objects.filter(student = self.user)
        self.assertEqual(self.requests[0].interval, 1)