from django.test import TestCase
from ...models import Transfer, User
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
import datetime

class TransferTest(TestCase):
    """Unit tests of the Transfer model."""

    fixtures = [
        'lessons/tests/fixtures/default_user.json'
    ]
    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.transfer = Transfer(
            student=self.user,
            amount= Decimal('25.55'),
            date = timezone.now()
        )
        self.transfer.save()
    
    def test_transfer_is_valid(self):
        self._assert_transfer_is_valid()

    def test_user_is_required(self):
        self.transfer.student = None
        self._assert_transfer_is_invalid()
    
    def test_amount_must_be_a_float(self):
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