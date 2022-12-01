from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import Request, Booking
from .helpers import get_requests, get_users_bookings, get_all_bookings
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LogInForm, RequestForm, BookingForm
from django.contrib.auth import login, logout
from .decorators import student_required, director_required, admin_required
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse


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

class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """View that handles log in."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = 'feed'

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)

        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


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

class SignUpView(LoginProhibitedMixin, FormView):
    """View that signs up user."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)

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
                topic=form.cleaned_data.get('topic'),
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

def manage_admin(request):
    admin_list = User.objects.filter(is_admin=True)
    return render(request, 'manage_admin.html', {'admin_list': admin_list})

def delete_admin(request, email):
    if(User.objects.filter(username = email)):
        User.objects.filter(username = email).delete()
        messages.add_message(request, messages.SUCCESS, "Admin deleted!")
        return redirect('manage_admin')
    else:
        messages.add_message(request, messages.ERROR, "Couldn't delete admin")

def create_admin(request):
