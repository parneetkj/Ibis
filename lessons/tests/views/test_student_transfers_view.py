from django.test import TestCase
from django.urls import reverse
from lessons.models import Invoice, User, Booking
from lessons.forms import SelectStudentForm
from lessons.helpers import calculate_student_balance
from lessons.tests.helpers import reverse_with_next

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
        self.url = reverse('student_transfers')

    def test_student_transfer_url(self):
        self.assertEqual(self.url, '/student_transfers/')
    
    def test_get_student_transfers(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_transfers.html')
        self.assertContains(response, self.user.balance)
    
    def test_get_student_transfer_redirects_if_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    