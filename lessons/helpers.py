from .models import Request

def get_requests(user):
    # To do: Change to user when implemented
    requests = Request.objects.filter(student=user)
    return requests


from django.urls import reverse

class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

