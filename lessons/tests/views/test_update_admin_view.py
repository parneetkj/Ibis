from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.forms import UpdateAdminForm
from django.contrib.auth.hashers import check_password

class UpdateAdminViewTestCase(TestCase):
    """Test case of edit booking view"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_director.json',
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='bobdoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')
        self.adminList = User.objects.filter(is_admin=True)
        self.form_input = {
            'first_name': 'Petraa',
            'last_name': 'Pickless',
            'username': 'petra_pickles@example.org',
            'is_director': False,
            'password': 'Password123'

        }

    def test_update_admin_displays_correct_page(self):
        self.client.login(username=self.user.username, password='Password123')
        update_admin_url = reverse('update_admin', kwargs={'pk': self.adminList[0].pk})
        response = self.client.get(update_admin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_admin.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UpdateAdminForm))
        self.assertContains(response, "Petra")

    def test_update_correctly_saves(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('update_admin', kwargs={'pk': self.adminList[0].pk})
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_admin.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UpdateAdminForm))
        self.assertContains(response, "Petra")

    def test_redirect_with_incorrect_admin_id(self):
        self.client.login(username=self.user.username, password='Password123')
        update_admin_url = reverse('update_admin', kwargs={'pk': (User.objects.count()) +100})
        redirect_url = reverse('manage_admin')
        response = self.client.get(update_admin_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'manage_admin.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_successful_update_of_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        request_url = reverse('update_admin', kwargs={'pk': self.adminList[0].pk})
        before_count = User.objects.count()
        response = self.client.post(request_url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(before_count, after_count)
        response_url = reverse('manage_admin')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'manage_admin.html')
        user = User.objects.get(username='petra_pickles@example.org')
        self.assertEqual(user.first_name, 'Petraa')
        self.assertEqual(user.last_name, 'Pickless')
        self.assertEqual(user.is_director, False)
        self.assertEqual(user.is_admin, True)
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
