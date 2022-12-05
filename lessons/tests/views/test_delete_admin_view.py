from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.tests.helpers import reverse_with_next

class DeleteAdminViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_director.json',
        'lessons/tests/fixtures/default_admin.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='bobdoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')
        self.url = reverse('delete_admin', kwargs={'email': self.admin.username})

    def test_get_delete_admin_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_delete_admin_redirects_director_correctly(self):
        self.client.login(username=self.user.username, password='Password123')
        redirect_url = reverse('manage_admin')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'manage_admin.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_delete_admin_correctly(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = User.objects.filter(is_admin=True).count()
        email_admin = User.objects.get(username=self.admin.username)
        delete_admin_url = reverse('delete_admin', kwargs={'email':email_admin})
        redirect_url = reverse('manage_admin')
        response = self.client.get(delete_admin_url, follow = True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200, fetch_redirect_response=True)
        after_count = User.objects.filter(is_admin=True).count()
        self.assertEqual(before_count-1, after_count)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_delete_admin_redirects_if_not_found(self):
        self.client.login(username=self.user.username, password='Password123')
        delete_admin_url = reverse('delete_admin', kwargs={'email': 'peterdoe@example.org'})
        redirect_url = reverse('manage_admin')
        response = self.client.get(delete_admin_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'manage_admin.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
