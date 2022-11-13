from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .forms import RequestForm
from .models import Request
from .helpers import get_requests


# Create your views here.
def feed(request):
    form = RequestForm()
    # Needs to be filtered by user
    requests = get_requests(None)
    return render(request, 'feed.html', {'form' : form, 'requests' : requests})

def new_request(request):
    if request.method == 'POST':
        #Should check for authenticated user
        form = RequestForm(request.POST)
        if form.is_valid():
            Request.objects.create(
                student=form.cleaned_data.get('student'),
                availability=form.cleaned_data.get('availability'),
                amount=form.cleaned_data.get('amount'),
                interval=form.cleaned_data.get('interval'),
                duration=form.cleaned_data.get('duration'),
                topic=form.cleaned_data.get('topic'),
                teacher=form.cleaned_data.get('teacher')
            )
            return redirect('feed')
        else:
            # Needs to be filtered by user
            requests = get_requests(None)
            return render(request, 'feed.html', {'form': form, 'requests' : requests})

    else:
        return HttpResponseForbidden

def booking(request):
    form = RequestForm()
    requests = get_requests(None)
    return render(request, 'booking.html', {'form' : form, 'requests' : requests})
