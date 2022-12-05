"""Unit tests of the Term model."""

from django.test import TestCase
from ...models import Term
from django.core.exceptions import ValidationError

class TermModelTest(TestCase):
    """Unit tests of the Term model."""

    def setUp(self):
        self.term = Term(
            start_date="2022-01-01",
            end_date="2022-01-31"
        )

    def test_valid_term(self):
        self._assert_term_is_valid()

    def test_start_date_should_not_be_blank(self):
        self.term.start_date = ""
        self._assert_term_is_invalid()

    def test_end_date_should_not_be_blank(self):
        self.term.start_date = ""
        self._assert_term_is_invalid()

    def _assert_term_is_valid(self):
        try:
            self.term.full_clean()
        except ValidationError:
            self.fail("Test request should be valid")

    def _assert_term_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.term.full_clean()

