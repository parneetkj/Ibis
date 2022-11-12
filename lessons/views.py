from django.shortcuts import render, redirect
from .forms import RequestForm
from .models import Request
from django.http import HttpResponseForbidden

# Create your views here.
def feed(request):
    form = RequestForm()
    return render(request, 'feed.html', {'form' : form})

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
            return render(request, 'feed.html', {'form': form})
    else:
        return HttpResponseForbidden