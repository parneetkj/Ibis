from django.test import TestCase
from ...models import Transfer, User, Invoice, Booking
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
import datetime
from lessons.helpers import calculate_student_balance

class TransferTest(TestCase):
    """Unit tests of the Transfer model."""

    fixtures = [
        'lessons/tests/fixtures/default_user.json'
    ]
    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')

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
        self.invoice = Invoice.objects.get(booking=self.booking)
        self.transfer = Transfer(
            invoice=self.invoice,
            amount= Decimal('25.55'),
            date = timezone.now()
        )
        self.transfer.save()
        calculate_student_balance(self.user)
    
    def test_transfer_is_valid(self):
        self._assert_transfer_is_valid()

    def test_invoice_is_required(self):
        self.transfer.invoice = None
        self._assert_transfer_is_invalid()
    
    def test_amount_must_be_a_Decimal(self):
        self.transfer.amount = "Test"
        self._assert_transfer_is_invalid()

    def test_amount_is_required(self):
        self.transfer.amount = None
        self._assert_transfer_is_invalid()
    
    def test_amount_is_no_more_than_2_dp(self):
        self.transfer.amount = 3.139
        self._assert_transfer_is_invalid()
    
    def test_amount_is_no_more_than_10_digits(self):
        self.transfer.amount = 12345.678901
        self._assert_transfer_is_invalid()

    def test_date_is_a_timedate_instance(self):
        self.assertTrue(isinstance(self.transfer.date, datetime.datetime))

    def _assert_transfer_is_valid(self):
        try:
            self.transfer.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_transfer_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.transfer.full_clean()