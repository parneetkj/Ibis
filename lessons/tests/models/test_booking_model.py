"""Unit tests of the Booking model."""
from django.test import TestCase
from ...models import Booking, User, Term
from django.core.exceptions import ValidationError

class BookingTest(TestCase):
    """Unit tests of the Booking model."""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_terms.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.term = Term.objects.get(pk=2)
        self.start_date = self.term.start_date
        self.end_date = self.term.end_date

        self.booking = Booking(
            student=self.user,
            term=self.term,
            start_date=self.start_date,
            end_date=self.end_date,
            day="Monday",
            time="14:30",
            duration=30,
            interval=1,
            teacher="Mrs.Smith",
            topic="Violin",
        )

    def test_valid_booking(self):
        self._assert_booking_is_valid()

    def test_student_should_not_be_blank(self):
        self.booking.student = None
        self._assert_booking_is_invalid()

    def test_day_should_not_be_blank(self):
        self.booking.day = ""
        self._assert_booking_is_invalid()

    def test_time_should_not_be_blank(self):
        self.booking.day = ""
        self._assert_booking_is_invalid()

    def test_start_date_should_not_be_blank(self):
        self.booking.start_date = ""
        self._assert_booking_is_invalid()
    
    def test_end_date_should_not_be_blank(self):
        self.booking.start_date = ""
        self._assert_booking_is_invalid()

    def test_duration_can_be_15(self):
        self.booking.duration = 15
        self._assert_booking_is_valid()

    def test_duration_can_be_30(self):
        self.booking.duration = 30
        self._assert_booking_is_valid()

    def test_duration_can_be_45(self):
        self.booking.duration = 45
        self._assert_booking_is_valid()

    def test_duration_can_be_60(self):
        self.booking.duration = 60
        self._assert_booking_is_valid()

    def test_duration_cannot_be_non_option(self):
        self.booking.duration = 61
        self._assert_booking_is_invalid()

    def test_interval_should_not_be_less_than_1(self):
        self.booking.interval = 0
        self._assert_booking_is_invalid()

    def test_interval_should_not_be_more_than_4(self):
        self.booking.interval = 5
        self._assert_booking_is_invalid()

    def test_teacher_may_not_be_blank(self):
        self.booking.teacher = ""
        self._assert_booking_is_invalid()

    def test_teacher_should_not_be_too_long(self):
        self.booking.teacher = "X" * 101
        self._assert_booking_is_invalid()

    def test_topic_may_not_be_blank(self):
        self.booking.topic = ""
        self._assert_booking_is_invalid()

    def _assert_booking_is_valid(self):
        try:
            self.booking.full_clean()
        except ValidationError:
            self.fail("Test request should be valid")

    def _assert_booking_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.booking.full_clean()
