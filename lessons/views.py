from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import RequestForm
from .models import Request
from .helpers import get_requests
from .models import User
from .forms import SignUpForm

from .forms import LogInForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from .helpers import login_prohibited
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.urls import reverse

from .decorators import student_required, admin_required, director_required

# Create your views here.
def home_page(request):
    return render(request, 'home_page.html')

@login_required
@student_required
def feed(request):
    form = RequestForm()
    requests = get_requests(request.user)
    return render(request, 'feed.html', {'form' : form, 'requests' : requests})


@login_required
@student_required
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
@student_required
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
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
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
@student_required
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

@login_required
@admin_required
def pending_requests(request):
    form = RequestForm()
    requests = requests = Request.objects.filter()
    return render(request, 'pending_requests.html', {'form' : form, 'requests' : requests})

@login_required
@admin_required
def new_booking(request, id):
    try:
        pending_request = Request.objects.get(id=id)
    except:
        messages.add_message(request, messages.ERROR, "Request could not be found!")
        return redirect('feed')
    if request.method == 'POST':
        form = BookingForm(instance = pending_request, data = request.POST)
        if form.is_valid():
            Booking.objects.create(
                student=request.user,
                day=form.cleaned_data.get('day'),
                time=form.cleaned_data.get('time'),
                start_date=form.cleaned_data.get('start_date'),
                duration=form.cleaned_data.get('duration'),
                interval=form.cleaned_data.get('interval'),
                teacher=form.cleaned_data.get('teacher'),
                no_of_lessons=form.cleaned_data.get('no_of_lessons'),
            )
            Request.objects.filter(id=id).delete()
            return redirect('feed')
        else:
            return render(request, 'new_booking.html', {'form': form, 'request': pending_request})
    else:
        form = BookingForm(instance = pending_request)
        return render(request, 'new_booking.html', {'form': form, 'request' : pending_request})

@login_required
def bookings(request):
    if request.user.is_student:
        messages.add_message(request, messages.INFO, "To edit or delete your bookings please contact your school administrator")
        bookings = get_users_bookings(request.user)
    else:
        bookings = get_all_bookings()
    return render(request, 'bookings.html', {'bookings' : bookings})

@login_required
@admin_required
def update_booking(request, id):
    try:
        booking_request = Booking.objects.get(pk=id)
    except:
        messages.add_message(request, messages.ERROR, "Booking could not be found!")
        return redirect('bookings')
        
    if request.method == 'POST':
        form = BookingForm(instance = booking_request, data = request.POST)
        if (form.is_valid()):
            messages.add_message(request, messages.SUCCESS, "Booking successfully updated!")
            form.save()
            return redirect('bookings')
        else:
            return render(request, 'update_booking.html', {'form': form, 'request' : booking_request})
    else:
        form = BookingForm(instance = booking_request)
        return render(request, 'update_booking.html', {'form': form, 'request' : booking_request})

@login_required
@admin_required
def delete_booking(request, id):
    if (Booking.objects.filter(pk=id)):
        Booking.objects.filter(pk=id).delete()
        messages.add_message(request, messages.SUCCESS, "Booking deleted!")
        return redirect('bookings')
    else:
        messages.add_message(request, messages.ERROR, "Sorry, an error occurred deleting your request.")    
        return redirect('bookings')
