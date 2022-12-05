from django.urls import reverse
from lessons.models import Request, Booking
class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

def reverse_with_next(url_name, next_url):
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url

def create_requests(user, from_count, to_count):
    """Create unique requests testing"""
    for count in range(from_count, to_count):
        topic_text = f'Topic__{count}'

        request = Request(
            student=user,
            date="2023-12-12",
            time="10:51",
            amount=5,
            interval=1,
            duration=60,
            topic = topic_text,
            teacher = "Ms.Test"
        )
        request.save()


def create_bookings(user, from_count, to_count):
    """Create unique bookings testing"""
    for count in range(from_count, to_count):
        teacher_text = f'Teacher__{count}'

        booking = Booking(
            student=user,
            day="Mon",
            start_date="2023-12-12",
            time="10:51",
            no_of_lessons=5,
            interval=1,
            duration=60,
            teacher = teacher_text,
            topic = "topic",
            cost='14.55'
        )
        booking.save()