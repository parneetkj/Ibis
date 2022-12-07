from django.shortcuts import render, redirect
from .models import Request, Booking, Invoice, Transfer, User
from .helpers import get_user_requests, get_all_requests, get_user_bookings, get_all_bookings, get_user_transfers, create_transfer, get_user_invoices, calculate_student_balance, get_invoice_transfers
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LogInForm, RequestForm, BookingForm, TransferForm, SelectStudentForm
from django.contrib.auth import login, logout
from .decorators import student_required, director_required, admin_required
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse
from django.core.exceptions import PermissionDenied

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



def home_page(request):
    return render(request, 'home_page.html')

@login_required
def feed(request):
    if request.user.is_student:
        calculate_student_balance(request.user)
        requests = len(get_user_requests(request.user))
        bookings = len(get_user_bookings(request.user))
    else:
        requests = len(get_all_requests())
        bookings = len(get_all_bookings())
    return render(request, 'feed.html', {'requests' : requests, 'bookings':bookings})


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

            return redirect('pending_requests')
            #return render(request, 'pending_requests.html', {'requests' : requests})
        else:
            return render(request, 'new_request.html', {'form': form})
    else:
        form = RequestForm()
        return render(request, 'new_request.html', {'form': form})


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


@login_required
def pending_requests(request):
    if request.user.is_student:
        requests = get_user_requests(request.user)
    else:
        requests = get_all_requests()
    return render(request, 'pending_requests.html', {'requests' : requests})
    

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
                student=pending_request.student,
                day=form.cleaned_data.get('day'),
                time=form.cleaned_data.get('time'),
                start_date=form.cleaned_data.get('start_date'),
                duration=form.cleaned_data.get('duration'),
                interval=form.cleaned_data.get('interval'),
                teacher=form.cleaned_data.get('teacher'),
                no_of_lessons=form.cleaned_data.get('no_of_lessons'),
                topic=form.cleaned_data.get('topic'),
                cost=form.cleaned_data.get('cost'),
            )
            booking_request = Booking.objects.all().latest('id')
            booking_request.generate_invoice()
            calculate_student_balance(booking_request.student)
            Request.objects.filter(id=id).delete()
            messages.add_message(request, messages.SUCCESS, "Booking successfully created!")
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
        bookings = get_user_bookings(request.user)
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
            Invoice.objects.get(booking=booking_request).change_invoice_amount()
            calculate_student_balance(booking_request.student)
            return redirect('bookings')
        else:
            return render(request, 'update_booking.html', {'form': form, 'request' : booking_request})
    else:
        form = BookingForm(instance = booking_request)
        return render(request, 'update_booking.html', {'form': form, 'request' : booking_request})

@login_required
@admin_required
def delete_booking(request, id):
    try:
        booking = Booking.objects.get(pk=id)
    except:
        messages.add_message(request, messages.ERROR, "Sorry, an error occurred deleting your request.")    
        return redirect('bookings')
   
    student = booking.student
    booking.delete()
    calculate_student_balance(student)
    messages.add_message(request, messages.SUCCESS, "Booking deleted!")
    return redirect('bookings')

        
        
def log_out(request):
    logout(request)
    return redirect('home_page')

@login_required
def view_invoice(request, booking_id):
        try:
            booking_request = Booking.objects.get(pk=booking_id)
            invoice = Invoice.objects.get(booking=booking_request)
            transfers = Transfer.objects.filter(invoice=invoice)
        except:
            messages.add_message(request, messages.ERROR, "Invoice could not be found!")
            return redirect('bookings')

        if(invoice.booking.student != request.user):
            if (request.user.is_student):
                messages.add_message(request, messages.ERROR, "Sorry, this is not your invoice!")
                return redirect('bookings')
        if (request.user.is_admin):
            if(invoice.is_paid == False):
                form = TransferForm()
                return render(request, 'view_invoice.html', {'invoice' : invoice, 'transfers':transfers, 'form':form})
            else:
                return render(request, 'view_invoice.html', {'invoice' : invoice, 'transfers':transfers})
        else:
             return render(request, 'view_invoice.html', {'invoice' : invoice, 'transfers':transfers})
@login_required
def transfers(request):
    if (request.user.is_student):
        return redirect('feed')
    if request.method == 'POST':
        form = SelectStudentForm(request.POST)
        if form.is_valid():
            student = User.objects.get(id=form.cleaned_data.get('student').pk)
            return student_transfers(request,student.pk)  
        else:
            form = SelectStudentForm()
            messages.add_message(request, messages.ERROR, "Sorry, could not find this student!")
            return render(request, 'transfers.html', {'form' : form})
            
    else:
        form = SelectStudentForm()
        return render(request, 'transfers.html', {'form' : form})

@login_required
def student_transfers(request, student_id=None):
    if(student_id==None):
        student = User.objects.get(id=request.user.pk)
    else:
        student = User.objects.get(id=student_id)
    user_invoices = get_user_invoices(student)
    user_transfers = get_user_transfers(student)

    return render(request, 'student_transfers.html', {'transfers' : user_transfers,'invoices':user_invoices, 'student':student})


@login_required
@admin_required
def pay_invoice(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except:
        messages.add_message(request, messages.ERROR, "Sorry, could not locate the invoice!")
        return redirect('bookings')
        
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            if(invoice.is_paid):
                return render(request, 'view_invoice.html', {'invoice' : invoice})

            create_transfer(invoice, form.cleaned_data.get('amount'))
            invoice.check_if_paid()
            calculate_student_balance(invoice.booking.student) 
            messages.add_message(request, messages.SUCCESS, "Transfer added!")
        
        invoice = Invoice.objects.get(id=invoice_id)
        form = TransferForm()
        transfers = get_invoice_transfers(invoice)
        return render(request, 'view_invoice.html', {'invoice' : invoice, 'transfers':transfers, 'form':form})
    else:
        transfers = get_invoice_transfers(invoice)
        if(invoice.is_paid):
            return render(request, 'view_invoice.html', {'invoice' : invoice,'transfers':transfers})
        else:
            form = TransferForm()
            return render(request, 'view_invoice.html', {'invoice' : invoice, 'form':form,'transfers':transfers})
