from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Booking, Invoice
from lessons.tests.helpers import reverse_with_next
from lessons.forms import TransferForm

class SubmitTransferViewTestCase(TestCase):
    """Test case of feed view"""
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
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
            price=300.25,
            is_paid=False
        )
        self.InvoiceData.save()

        self.form_input = {
            'amount_paid' : 300.25
        }

    def test_submit_transfer_saves_correctly(self):
        #TEST REMOVE WHEN GENERATE INVOICE IS IMPLEMENTED
        User.objects.get(username=self.user.username).decrease_balance(300.25)
        #-----------------------------------------------
        self.client.login(username=self.admin.username, password='Password123')
        before_count = Invoice.objects.count()
        before_amount = User.objects.get(username=self.user.username).balance
        transfer_url = reverse('submit_transfer', kwargs={'invoice_id': self.InvoiceData.pk})
        response = self.client.post(transfer_url, self.form_input, follow=True)
        after_count = Invoice.objects.count()
        after_amount = User.objects.get(username=self.user.username).balance
        self.assertEqual(after_count, before_count)
        self.assertNotEqual(before_amount,after_amount)
        self.assertEqual(0, after_amount)
        response_url = reverse('bookings')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'bookings.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

        invoice = Invoice.objects.get(booking = self.bookingData)
        self.assertEqual(invoice.price, 300.25)
        self.assertTrue(invoice.is_paid)

    def test_submit_transfer_saves_correctly_with_less_than_invoice_amount(self):
        #TEST REMOVE WHEN GENERATE INVOICE IS IMPLEMENTED
        User.objects.get(username=self.user.username).decrease_balance(300.25)
        #-----------------------------------------------
        self.form_input['amount_paid'] = 150.25
        self.client.login(username=self.admin.username, password='Password123')
        before_count = Invoice.objects.count()
        before_amount = User.objects.get(username=self.user.username).balance
        transfer_url = reverse('submit_transfer', kwargs={'invoice_id': self.InvoiceData.pk})
        response = self.client.post(transfer_url, self.form_input, follow=True)
        after_count = Invoice.objects.count()
        after_amount = User.objects.get(username=self.user.username).balance
        self.assertEqual(after_count, before_count)
        self.assertNotEqual(before_amount,after_amount)
        self.assertEqual(-150.0, after_amount)
        response_url = reverse('bookings')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'bookings.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

        invoice = Invoice.objects.get(booking = self.bookingData)
        self.assertEqual(invoice.price, 300.25)
        self.assertFalse(invoice.is_paid)
        self.assertIsNotNone(invoice.date_paid)
    
    def test_submit_transfer_saves_correctly_with_more_than_invoice_amount(self):
        #TEST REMOVE WHEN GENERATE INVOICE IS IMPLEMENTED
        User.objects.get(username=self.user.username).decrease_balance(300.25)
        #-----------------------------------------------
        self.form_input['amount_paid'] = 400
        self.client.login(username=self.admin.username, password='Password123')
        before_count = Invoice.objects.count()
        before_amount = User.objects.get(username=self.user.username).balance
        transfer_url = reverse('submit_transfer', kwargs={'invoice_id': self.InvoiceData.pk})
        response = self.client.post(transfer_url, self.form_input, follow=True)
        after_count = Invoice.objects.count()
        after_amount = User.objects.get(username=self.user.username).balance
        self.assertEqual(after_count, before_count)
        self.assertNotEqual(before_amount,after_amount)
        self.assertEqual(99.75, after_amount)
        response_url = reverse('bookings')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'bookings.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

        invoice = Invoice.objects.get(booking = self.bookingData)
        self.assertEqual(invoice.price, 300.25)
        self.assertTrue(invoice.is_paid)
        self.assertIsNotNone(invoice.date_paid)
    
    def test_redirect_with_incorrect_invoice_id(self):
        self.client.login(username=self.admin.username, password='Password123')
        transfer_url = reverse('submit_transfer', kwargs={'invoice_id': Invoice.objects.count()+1})
        redirect_url = reverse('bookings')
        response = self.client.post(transfer_url, self.form_input, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'bookings.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_redirect_when_student_logged_in(self):
        self.client.login(username=self.user.username, password='Password123')
        transfer_url = reverse('submit_transfer', kwargs={'invoice_id': self.InvoiceData.pk})
        redirect_url = reverse('feed')
        response = self.client.post(transfer_url, self.form_input, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_submit_transfer_get_request_is_forbidden(self):
        transfer_url = reverse('submit_transfer', kwargs={'invoice_id': self.InvoiceData.pk})
        self.client.login(username=self.admin.username, password='Password123')
        response = self.client.get(transfer_url, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_form_is_validated_correctly(self):
        self.form_input['amount_paid'] = "Apple"
        self.client.login(username=self.admin.username, password='Password123')
        transfer_url = reverse('submit_transfer', kwargs={'invoice_id': self.InvoiceData.pk})
        response = self.client.post(transfer_url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_transfer.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TransferForm))
        self.assertTrue(form.is_bound)