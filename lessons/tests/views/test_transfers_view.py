"""Test case of transfer view"""
from django.test import TestCase
from django.urls import reverse
from lessons.forms import TransferForm
from lessons.models import User, Transfer, Booking
from lessons.tests.helpers import reverse_with_next

class TransfersViewTestCase(TestCase):
    """Test case of bookings view"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json',
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.url = reverse('transfers')
        self.user = User.objects.get(username='johndoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')

        self.booking = Booking(
            student=self.user,
            day="Monday",
            time="14:30",
            start_date="2022-11-16",
            duration=30,
            interval=1,
            teacher="Mrs.Smith",
            no_of_lessons=4,
            topic="Violin",
            cost=5
        )
        self.booking.save()
        self.booking.generate_invoice()
        self.form_input = {'student': self.user.pk, 'amount': '40'}
    
    def test_transfers_url(self):
        self.assertEqual(self.url,'/transfers/')
    
    def test_get_transfers(self):
        self.client.login(username=self.admin.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transfers.html')
    
    def test_get_transfers_blocked_for_students(self):
        self.client.login(username=self.user.username, password='Password123')
        redirect_url = reverse('feed')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_successful_new_transfer(self):
        self.client.login(username=self.admin.username, password="Password123")
        before_balance = self.user.balance
        before_count = Transfer.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Transfer.objects.count()
        after_balance = User.objects.get(id=self.user.pk).balance
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(after_balance, before_balance+40)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transfers.html')
        
    def test_unsuccessful_new_transfer(self):
        self.client.login(username=self.admin.username, password="Password123")
        count_before = Transfer.objects.count()
        self.form_input['amount'] = '40.94949'
        response = self.client.post(self.url, self.form_input)
        count_after = Transfer.objects.count()
        self.assertEqual(count_after, count_before)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transfers.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TransferForm))
        
