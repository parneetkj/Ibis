from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import User, Request, Booking
from .helpers import get_requests, get_bookings
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LogInForm, RequestForm, BookingForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home_page(request):
    return render(request, 'home_page.html')

@login_required
def feed(request):
    form = RequestForm()
    requests = get_requests(request.user)
    bookings = get_bookings(None)

    return render(request, 'feed.html', {'form' : form, 'requests' : requests, 'bookings' : bookings})

@login_required
def new_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            Request.objects.create(
                student=request.user,
                date=form.cleaned_data.get('date'),
                time=form.cleaned_data.get('time'),
                amount=form.cleaned_data.get('amount'),
                interval=form.cleaned_data.get('interval'),
                duration=form.cleaned_data.get('duration'),
                topic=form.cleaned_data.get('topic'),
                teacher=form.cleaned_data.get('teacher')
            )
            return redirect('feed')
        else:
            requests = get_requests(request.user)
            return render(request, 'feed.html', {'form': form, 'requests' : requests})
    else:
        return HttpResponseForbidden


@login_required
def update_request(request, id):
    try:
        lesson_request = Request.objects.get(pk=id)
    except:
        messages.add_message(request, messages.ERROR, "Request could not be found!")
        return redirect('feed')
        
    if request.method == 'POST':
        form = RequestForm(instance = lesson_request, data = request.POST)
        if (form.is_valid()):
            messages.add_message(request, messages.SUCCESS, "Request updated!")
            form.save()
            return redirect('feed')
        else:
            return render(request, 'update_request.html', {'form': form, 'request' : lesson_request})
    else:
        form = RequestForm(instance = lesson_request)
        return render(request, 'update_request.html', {'form': form, 'request' : lesson_request})
    
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        next = request.POST.get('next') or ''
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                redirect_url = next or 'feed'
                return redirect(redirect_url)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    else:
        next = request.GET.get('next') or ''
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form, 'next': next})

@login_required
def delete_request(request, id):
    if (Request.objects.filter(pk=id)):
        Request.objects.filter(pk=id).delete()
        messages.add_message(request, messages.SUCCESS, "Request deleted!")
        return redirect('feed')
    else:
        messages.add_message(request, messages.ERROR, "Sorry, an error occurred deleting your request.")    
        return redirect('feed')

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

def log_out(request):
    logout(request)
    return redirect('home_page')

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
