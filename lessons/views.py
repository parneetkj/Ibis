from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import User, Request, Booking
from .helpers import get_requests, get_bookings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm, RequestForm, BookingForm

def home_page(request):
    return render(request, 'home_page.html')
# Create your views here.
def feed(request):
    form = RequestForm()
    # Needs to be filtered by user
    requests = get_requests(None)
    bookings = get_bookings(None)

    return render(request, 'feed.html', {'form' : form, 'requests' : requests, 'bookings' : bookings})

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


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def pending_requests(request):
    form = RequestForm()
    # Needs to be filtered by user
    requests = get_requests(None)
    return render(request, 'pending_requests.html', {'form' : form, 'requests' : requests})

def new_booking(request, request_id):
    pending_request = Request.objects.get(id=request_id)
    if request.method == 'POST':
        form = BookingForm(instance = pending_request, data = request.POST)
        if form.is_valid():
            Booking.objects.create(
                student=form.cleaned_data.get('student'),
                day=form.cleaned_data.get('day'),
                time=form.cleaned_data.get('time'),
                start_date=form.cleaned_data.get('start_date'),
                duration=form.cleaned_data.get('duration'),
                interval=form.cleaned_data.get('interval'),
                teacher=form.cleaned_data.get('teacher'),
                no_of_lessons=form.cleaned_data.get('no_of_lessons'),
            )
            Request.objects.filter(id=request_id).delete()
            return redirect('feed')
        else:
            return render(request, 'new_booking.html', {'form': form, 'request': pending_request})
    else:
        form = BookingForm(instance = pending_request)
        return render(request, 'new_booking.html', {'form': form, 'request' : pending_request})
