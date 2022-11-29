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
        self.requests = Request.objects.filter(student = self.user)

    def test_update_request_displays_correct_page(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('update_request', kwargs={'id': self.requests[0].pk})
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_request.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RequestForm))
        self.assertContains(response, "Mrs.Smith")

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
        self.assertContains(response, "Mrs.Smith")

        #Change a value in the form
        #Check against the database