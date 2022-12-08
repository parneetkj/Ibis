from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.tests.helpers import reverse_with_next

class PromoteAdminViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_director.json',
        'lessons/tests/fixtures/default_admin.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='bobdoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')
        self.adminList = User.objects.filter(is_admin=True).filter(is_director=False)
        self.url = reverse('promote_admin', kwargs={'pk': self.admin.id})

    def test_get_promote_admin_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_promote_admin_redirects_director_correctly(self):
        self.client.login(username=self.user.username, password='Password123')
        redirect_url = reverse('manage_admin')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'manage_admin.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_promote_admin_successful(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('update_admin', kwargs={'pk': self.adminList[0].pk})
        before_count = User.objects.filter(is_admin=True).filter(is_director=False).count()
        change_admin = User.objects.get(id=self.admin.id)
        promote_admin_url = reverse('promote_admin', kwargs={'pk': self.adminList[0].pk})
        redirect_url = reverse('manage_admin')
        response = self.client.get(promote_admin_url, follow = True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

        after_count = User.objects.filter(is_admin=True).filter(is_director=True).count()
        self.assertEqual(before_count+1, after_count)

        self.assertTrue(change_admin.id, True)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_promote_admin_redirects_if_not_found(self):
        self.client.login(username=self.user.username, password='Password123')
        promote_admin_url = reverse('promote_admin', kwargs={'pk': (User.objects.count()) +100})
        redirect_url = reverse('manage_admin')
        response = self.client.get(promote_admin_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'manage_admin.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
