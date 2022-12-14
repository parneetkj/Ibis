from django.test import TestCase
from django.urls import reverse
from lessons.models import Invoice, User, Booking, Transfer
from lessons.tests.helpers import reverse_with_next
from lessons.helpers import calculate_student_balance

class PayInvoiceViewTestCase(TestCase):
    """Test case of new request view"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json',
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
        self.url = reverse('pay_invoice', kwargs={'invoice_id': self.invoice.pk})
        self.form_input = {'amount': '40'}

    def test_pay_invoice_url(self):
        self.assertEqual(self.url,f'/pay_invoice/{self.booking.pk}')
    
    def test_get_pay_invoice(self):
        self.client.login(username=self.admin.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_invoice.html')
    
    def test_get_pay_invoice_redirects_when_not_logged_in(self):
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_get_pay_invoice_redirects_for_students(self):
        self.client.login(username=self.user.username, password='Password123')
        redirect_url = reverse('feed')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
    
    def test_get_pay_invoice_sets_invoice_correctly_with_full_amount(self):
        self.client.login(username=self.admin.username, password='Password123')
        self.assertEqual(self.user.balance, -40)

        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_invoice.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        
        self.invoice = Invoice.objects.get(id=self.booking.pk)
        self.user = User.objects.get(username='johndoe@example.org')

        self.assertEqual(self.user.balance, 0)
        self.assertTrue(self.invoice.is_paid)
        self.assertIsNotNone(self.invoice.date_paid)
    
    def test_get_pay_invoice_sets_invoice_correctly_with_under_amount(self):
        self.client.login(username=self.admin.username, password='Password123')
        self.assertEqual(self.user.balance, -40)
        self.form_input['amount'] = '30'

        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_invoice.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        
        self.invoice = Invoice.objects.get(id=self.booking.pk)
        self.user = User.objects.get(username='johndoe@example.org')

        self.assertEqual(self.user.balance, -10)
        self.assertFalse(self.invoice.is_paid)
        self.assertIsNone(self.invoice.date_paid)
    
    def test_get_pay_invoice_sets_invoice_correctly_with_over_amount(self):
        self.client.login(username=self.admin.username, password='Password123')
        self.assertEqual(self.user.balance, -40)
        self.form_input['amount'] = '50'

        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_invoice.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        
        self.invoice = Invoice.objects.get(id=self.booking.pk)
        self.user = User.objects.get(username='johndoe@example.org')

        self.assertEqual(self.user.balance, 10)
        self.assertTrue(self.invoice.is_paid)
        self.assertIsNotNone(self.invoice.date_paid)
    
    def test_get_pay_invoice_loads_view_invoice(self):
        self.client.login(username=self.admin.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_invoice.html')
    
    def test_get_pay_invoice_redirects_if_invoice_not_found(self):
        self.client.login(username=self.admin.username, password='Password123')
        self.url = reverse('pay_invoice', kwargs={'invoice_id': Invoice.objects.count() +1})
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('bookings')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'bookings.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_post_pay_invoice_redirects_if_invoice_is_paid(self):
        self.client.login(username=self.admin.username, password='Password123')
        self.assertEqual(self.user.balance, -40)
        form_input = {'amount': '40'}

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.invoice = Invoice.objects.get(id=self.booking.pk)
        self.user = User.objects.get(username='johndoe@example.org')
        self.assertEqual(self.user.balance, 0)
        self.assertTrue(self.invoice.is_paid)
        self.assertIsNotNone(self.invoice.date_paid)

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_invoice.html')
    
    def test_post_pay_invoice_rejects_invalid_form(self):
        self.client.login(username=self.admin.username, password='Password123')
        form_input = {'amount': '99.999'}
        before_count = Transfer.objects.count()

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_invoice.html')
        after_count = Transfer.objects.count()
        self.assertEqual(before_count,after_count)
    
    def test_get_pay_invoice_hides_admin_form_when_invoice_paid(self):
        self.client.login(username=self.admin.username, password='Password123')
        self.assertEqual(self.user.balance, -40)
        form_input = {'amount': '40'}

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.invoice = Invoice.objects.get(id=self.booking.pk)
        self.user = User.objects.get(username='johndoe@example.org')
        self.assertEqual(self.user.balance, 0)
        self.assertTrue(self.invoice.is_paid)
        self.assertIsNotNone(self.invoice.date_paid)

        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_invoice.html')
        self.assertContains(response, "Paid!")
        self.assertNotContains(response,'form')