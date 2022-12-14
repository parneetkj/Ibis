from django.test import TestCase
from ...models import Request, User
from django.core.exceptions import ValidationError
import datetime


class RequestTest(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
    ]
    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.request = Request(
            student=self.user,
            date = '2023-12-12',
            time = '20:20',
            amount=4,
            interval=1,
            duration=30,
            topic="Violin",
            teacher='Mrs.Smith'
        )
    
    def test_valid_request(self):
        self._assert_request_is_valid()
        
    def test_student_should_not_be_blank(self):
        self.request.student = None
        self._assert_request_is_invalid()


    def test_date_should_not_be_blank(self):
        self.request.date = ""
        self._assert_request_is_invalid()
    
    def test_date_should_be_a_valid_date(self):
        self.request.date = "4-20-08"
        self._assert_request_is_invalid()


    def test_time_should_not_be_blank(self):
        self.request.time = ""
        self._assert_request_is_invalid()

    def test_time_should_be_a_valid_time(self):
        self.request.date = "25:61"
        self._assert_request_is_invalid()


    def test_amount_should_not_be_less_than_1(self):
        self.request.amount = 0
        self._assert_request_is_invalid()
    
    def test_amount_should_not_be_more_than_50(self):
        self.request.amount = 51
        self._assert_request_is_invalid()


    def test_interval_should_not_be_less_than_1(self):
        self.request.interval = 0
        self._assert_request_is_invalid()

    def test_interval_should_not_be_more_than_4(self):
        self.request.interval = 5
        self._assert_request_is_invalid()
    

    def test_duration_can_be_15(self):
        self.request.duration = 15
        self._assert_request_is_valid()
    
    def test_duration_can_be_30(self):
        self.request.duration = 30
        self._assert_request_is_valid()
    
    def test_duration_can_be_45(self):
        self.request.duration = 45
        self._assert_request_is_valid()

    def test_duration_can_be_60(self):
        self.request.duration = 60
        self._assert_request_is_valid()
    
    def test_duration_cannot_be_non_option(self):
        self.request.duration = 61
        self._assert_request_is_invalid()


    def test_topic_may_be_blank(self):
        self.request.topic = ''
        self._assert_request_is_valid()

    def test_topic_should_not_be_too_long(self):
        self.request.topic = "X" * 51
        self._assert_request_is_invalid()


    def test_teacher_may_be_blank(self):
        self.request.teacher = ''
        self._assert_request_is_valid()
    
    def test_teacher_should_not_be_too_long(self):
        self.request.topic = "X" * 101
        self._assert_request_is_invalid()
    
    def test_status_is_in_progress_as_default(self):
        self.assertEqual(self.request.status, "In Progress")
    
    def _assert_request_is_valid(self):
        try:
            self.request.full_clean()
        except ValidationError:
            self.fail("Test request should be valid")
    
    def _assert_request_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.request.full_clean()