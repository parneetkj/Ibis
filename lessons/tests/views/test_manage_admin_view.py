from django.test import TestCase
from django.urls import reverse
from lessons.forms import RequestForm
from lessons.models import User
from lessons.tests.helpers import reverse_with_next

class ManageAdminViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_director.json',
        'lessons/tests/fixtures/default_admin.json',
    ]
    def setUp(self):
        self.url = reverse('manage_admin')
        self.user = User.objects.get(username='bobdoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')

    def test_manage_admin_url(self):
        self.assertEqual(self.url,'/manage_admin')

    def test_get_manage_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_admin.html')


    def test_get_show_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_filter_admins_in_view(self):
        self.client.login(username=self.user.username, password='Password123')
        admin_user = User.objects.get(username='petra.pickles@example.org')
        list_admins = User.objects.filter(is_admin=True)
        admin_first = list_admins.get(username=admin_user)
        self.assertEqual(admin_user.username, admin_first.username)
