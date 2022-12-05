from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Booking, Invoice
from lessons.forms import TransferForm
from lessons.tests.helpers import reverse_with_next

class AddTransferViewTestCase(TestCase):
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

        self.bookingData = Booking(
            student=self.user,
            day = 'Mon',
            start_date = '2023-12-12',
            time = '20:20',
            no_of_lessons=4,
            interval=1,
            duration=30,
            teacher='Mrs.Smith',
            topic = "violin"
        )
        self.bookingData.save()
        self.InvoiceData = Invoice(
            booking = self.bookingData,
            total_price=300.25,
            is_paid=False,
            part_payment =0,
        )
        self.InvoiceData.save()

        self.form_input = {
            'amount_paid' : 300.25
        }

    def test_add_transfer_displays_correct_page(self):
        self.client.login(username=self.admin.username, password='Password123')
        transfer_url = reverse('add_transfer', kwargs={'booking_id': self.InvoiceData.booking.pk})
        response = self.client.get(transfer_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_transfer.html')
        self.assertContains(response, self.user.pk)
        self.assertContains(response, self.bookingData.pk)
        form = response.context['form']
        self.assertTrue(isinstance(form, TransferForm))
    
    def test_redirect_with_incorrect_booking_id(self):
        self.client.login(username=self.admin.username, password='Password123')
        invoice_url = reverse('add_transfer', kwargs={'booking_id': Invoice.objects.count()+1})
        redirect_url = reverse('bookings')
        response = self.client.get(invoice_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'bookings.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
    
    def test_add_transfer_redirects_when_not_logged_in(self):
        transfer_url = reverse('add_transfer', kwargs={'booking_id': self.InvoiceData.booking.pk})
        response = self.client.get(transfer_url)
        redirect_url = reverse_with_next('log_in',transfer_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_students_cannot_access_add_transfer_page(self):
        self.client.login(username=self.user.username, password='Password123')
        transfer_url = reverse('add_transfer', kwargs={'booking_id': self.InvoiceData.booking.pk})
        # Students cannot access 'bookings' so therefore will redirect twice to feed
        redirect_url = reverse('feed')
        response = self.client.get(transfer_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    

