from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Booking, Invoice
from lessons.tests.helpers import reverse_with_next
from lessons.forms import TransferForm
from lessons.helpers import calculate_student_balance

class ViewInvoiceTestCase(TestCase):
    """Test case of feed view"""
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json',
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.other_user = User.objects.get(username='janedoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')

        self.booking = Booking(
            student=self.user,
            day = 'Mon',
            start_date = '2023-12-12',
            time = '20:20',
            no_of_lessons=4,
            interval=1,
            duration=30,
            teacher='Mrs.Smith',
            topic = "violin",
            cost=5
        )
        self.booking.save()
        self.booking.generate_invoice()
        calculate_student_balance(self.user)
        self.invoice = Invoice.objects.get(booking = self.booking)
        self.transfer_url = reverse('pay_invoice', kwargs={'invoice_id': self.invoice.pk})
    
    def test_view_invoice_displays_correct_page(self):
        self.client.login(username=self.user.username, password='Password123')
        invoice_url = reverse('view_invoice', kwargs={'booking_id': self.booking.pk})
        response = self.client.get(invoice_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_invoice.html')
        self.assertContains(response, "Not Paid!")

    def test_redirect_with_incorrect_booking_id(self):
        self.client.login(username=self.user.username, password='Password123')
        invoice_url = reverse('view_invoice', kwargs={'booking_id': Booking.objects.count()+1})
        redirect_url = reverse('bookings')
        response = self.client.get(invoice_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'bookings.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 2)

    def test_wrong_user_cannot_access_others_invoice(self):
        self.client.login(username=self.other_user.username, password='Password123')
        invoice_url = reverse('view_invoice', kwargs={'booking_id': self.booking.pk})
        redirect_url = reverse('bookings')
        response = self.client.get(invoice_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'bookings.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 2)

    def test_admin_can_access_any_invoice(self):
        self.client.login(username=self.admin.username, password='Password123')
        invoice_url = reverse('view_invoice', kwargs={'booking_id': self.booking.pk})
        response = self.client.get(invoice_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_invoice.html')
        self.assertContains(response, "Not Paid!")
        form = response.context['form']
        self.assertTrue(isinstance(form, TransferForm))
        self.assertFalse(form.is_bound)

    def test_view_invoice_redirects_when_not_logged_in(self):
        invoice_url = reverse('view_invoice', kwargs={'booking_id': self.booking.pk})
        response = self.client.get(invoice_url)
        redirect_url = reverse_with_next('log_in',invoice_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_admin_transfer_form_is_hidden_when_invoice_paid(self):
        self.client.login(username=self.admin.username, password='Password123')
        self.assertEqual(self.user.balance, -40)
        form_input = {'amount': '40'}

        response = self.client.post(self.transfer_url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.invoice = Invoice.objects.get(id=self.booking.pk)
        self.user = User.objects.get(username='johndoe@example.org')
        self.assertEqual(self.user.balance, 0)
        self.assertTrue(self.invoice.is_paid)
        self.assertIsNotNone(self.invoice.date_paid)

        invoice_url = reverse('view_invoice', kwargs={'booking_id': self.booking.pk})
        response = self.client.get(invoice_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_invoice.html')
        self.assertContains(response, "Paid!")
        self.assertNotContains(response,'form')
