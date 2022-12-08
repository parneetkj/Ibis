from django.test import TestCase
from django.urls import reverse
from lessons.models import Invoice, User, Booking
from lessons.tests.helpers import reverse_with_next
from lessons.forms import SelectStudentForm
from lessons.helpers import calculate_student_balance

class TransfersViewTestCase(TestCase):
    """Test case of new request view"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
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
        calculate_student_balance(self.user)
        self.invoice = Invoice.objects.get(booking = self.booking)
        self.url = reverse('transfers')
        self.form_input = {'student': self.user.pk}

    def test_transfer_url(self):
        self.assertEqual(self.url, '/transfers/')
    
    def test_get_transfers(self):
        self.client.login(username=self.admin.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transfers.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SelectStudentForm))
        self.assertFalse(form.is_bound)
    
    def test_get_transfer_redirects_if_student(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
    
    def test_valid_student_selection(self):
        self.client.login(username=self.admin.username, password="Password123")
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_transfers.html')
        self.assertContains(response, self.user.balance)

    def test_invalid_student_selection(self):
        self.form_input['student'] = User.objects.count()+1
        self.client.login(username=self.admin.username, password="Password123")
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transfers.html')
        self.assertNotContains(response, self.user.balance)
        form = response.context['form']
        self.assertTrue(isinstance(form, SelectStudentForm))
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)