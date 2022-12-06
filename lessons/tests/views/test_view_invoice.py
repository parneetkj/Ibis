from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Booking, Invoice
from lessons.tests.helpers import reverse_with_next

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

        self.bookingData = Booking(
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
        self.bookingData.save()
        self.bookingData.generate_invoice()
    
    def test_view_invoice_displays_correct_page(self):
        self.client.login(username=self.user.username, password='Password123')
        invoice_url = reverse('view_invoice', kwargs={'booking_id': self.bookingData.pk})
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
        invoice_url = reverse('view_invoice', kwargs={'booking_id': self.bookingData.pk})
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
        invoice_url = reverse('view_invoice', kwargs={'booking_id': self.bookingData.pk})
        response = self.client.get(invoice_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_invoice.html')
        self.assertContains(response, "Not Paid!")

    def test_view_invoice_redirects_when_not_logged_in(self):
        invoice_url = reverse('view_invoice', kwargs={'booking_id': self.bookingData.pk})
        response = self.client.get(invoice_url)
        redirect_url = reverse_with_next('log_in',invoice_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    