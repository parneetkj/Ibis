from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .forms import RequestForm
from .models import Request
from .helpers import get_requests
from .models import User
from .forms import SignUpForm
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
            # Needs to be filtered by user
            requests = get_requests(None)
            return render(request, 'feed.html', {'form': form, 'requests' : requests})

    else:
        return HttpResponseForbidden


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