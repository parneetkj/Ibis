from .models import Request

def get_requests(user):
    # To do: Change to user when implemented
    requests = Request.objects.filter(student=user)
    return requests




