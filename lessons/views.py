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


def home_page(request):
    return render(request, 'home_page.html')
# Create your views here.
@login_required
def feed(request):
    form = RequestForm()
    requests = get_requests(request.user)
    return render(request, 'feed.html', {'form' : form, 'requests' : requests})

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
    lesson_request = Request.objects.get(pk=id)
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


def delete_request(request, id):
    try:
        Request.objects.filter(pk=id).delete()
        messages.add_message(request, messages.SUCCESS, "Request deleted!")
        return redirect('feed')
    except:
        messages.add_message(request, messages.SUCCESS, "Sorry, an error occurred deleting your request.")    
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