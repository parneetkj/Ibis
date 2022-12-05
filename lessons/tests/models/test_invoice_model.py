"""Unit tests of the Booking model."""
from django.test import TestCase
from ...models import Booking, User, Invoice
from django.urls import reverse

class InvoiceTest(TestCase):
    """Unit tests of the Booking model."""

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
        self.form_input = {'student': self.user.pk, 'amount': '40'}
        

    def test_invoice_is_generated_correctly(self):
        self.booking.generate_invoice()
        invoice = Invoice.objects.get(booking=self.booking)

        self.assertEqual(invoice.booking, self.booking)
        self.assertIsNone(invoice.date_paid)
        self.assertFalse(invoice.is_paid)
        self.assertEqual(5*2*4,invoice.total_price)

    def test_invoice_update_correctly_when_total_is_transferred(self):
        self.booking.generate_invoice()
        self.client.login(username=self.admin.username, password='Password123')

        self.assertEqual(self.user.balance, -40)
        self.client.post(reverse('transfers'), self.form_input, follow=True)
        self.user = User.objects.get(username='johndoe@example.org')
        self.assertEqual(self.user.balance, 0)

        invoice = Invoice.objects.get(booking=self.booking)
        self.assertEqual(invoice.booking, self.booking)
        self.assertIsNotNone(invoice.date_paid)
        self.assertTrue(invoice.is_paid)
        self.assertEqual(5*2*4,invoice.total_price)

    def test_invoice_update_correctly_when_less_than_total_is_transferred(self):
        self.booking.generate_invoice()
        self.client.login(username=self.admin.username, password='Password123')
        self.form_input['amount'] = '30'

        self.assertEqual(self.user.balance, -40)
        self.client.post(reverse('transfers'), self.form_input, follow=True)
        self.user = User.objects.get(username='johndoe@example.org')
        self.assertEqual(self.user.balance, -10)

        invoice = Invoice.objects.get(booking=self.booking)
        self.assertEqual(invoice.booking, self.booking)
        self.assertIsNone(invoice.date_paid)
        self.assertFalse(invoice.is_paid)
        self.assertEqual(5*2*4,invoice.total_price)

    def test_invoice_update_correctly_when_more_than_total_is_transferred(self):
        self.booking.generate_invoice()
        self.client.login(username=self.admin.username, password='Password123')
        self.form_input['amount'] = '50' 

        self.assertEqual(self.user.balance, -40)
        self.client.post(reverse('transfers'), self.form_input, follow=True)
        self.user = User.objects.get(username='johndoe@example.org')
        self.assertEqual(self.user.balance,10)

        invoice = Invoice.objects.get(booking=self.booking)
        self.assertEqual(invoice.booking, self.booking)
        self.assertIsNotNone(invoice.date_paid)
        self.assertTrue(invoice.is_paid)
        self.assertEqual(5*2*4,invoice.total_price)