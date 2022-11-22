from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from .forms import RequestForm
from .models import Request
from .helpers import get_requests
from .models import User
from .forms import SignUpForm
from .forms import LogInForm
from django.contrib.auth import login
from django.contrib import messages


def home_page(request):
    return render(request, 'home_page.html')
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