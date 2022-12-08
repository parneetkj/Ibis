from django.test import TestCase, RequestFactory
from lessons.models import User, Request
from lessons.views import feed, home_page, SignUpView, LogInView, pending_requests, update_request, manage_admin, new_request, delete_request, pending_requests, new_booking, update_booking, delete_booking, bookings, manage_admin, create_admin, delete_admin, view_invoice, transfers, promote_admin, pay_invoice, update_admin
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from lessons.forms import LogInForm

class AnonymousUserTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_anonymous_access_home_page(self):
        request = self.factory.get('/')
        response = home_page(request)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_access_log_in(self):
        self.url = reverse('log_in')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_anonymous_access_sign_up(self):
        self.url = reverse('sign_up')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')

    def test_anonymous_access_feed_page(self):
        request = self.factory.get('/feed')
        self.user = AnonymousUser()
        request.user = self.user
        response = feed(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_update_request_page(self):
        request = self.factory.get('/update_request')
        self.user = AnonymousUser()
        request.user = self.user
        response = update_request(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_new_request_page(self):
        request = self.factory.get('/new_request')
        self.user = AnonymousUser()
        request.user = self.user
        response = new_request(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_delete_request_page(self):
        request = self.factory.get('/delete_request')
        self.user = AnonymousUser()
        request.user = self.user
        response = delete_request(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_pending_request_page(self):
        request = self.factory.get('/pending_requests')
        self.user = AnonymousUser()
        request.user = self.user
        response = pending_requests(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_bookings_page(self):
        request = self.factory.get('/bookings')
        self.user = AnonymousUser()
        request.user = self.user
        response = bookings(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_update_booking_page(self):
        request = self.factory.get('/update_booking')
        self.user = AnonymousUser()
        request.user = self.user
        response = update_booking(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_delete_booking_page(self):
        request = self.factory.get('/delete_booking')
        self.user = AnonymousUser()
        request.user = self.user
        response = delete_booking(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_new_booking_page(self):
        request = self.factory.get('/new_booking')
        self.user = AnonymousUser()
        request.user = self.user
        response = new_booking(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_view_invoice_page(self):
        request = self.factory.get('/view_invoice')
        self.user = AnonymousUser()
        request.user = self.user
        response = view_invoice(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_transfers(self):
        request = self.factory.get('/create_admin')
        self.user = AnonymousUser()
        request.user = self.user
        response = transfers(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_pay_invoice_page(self):
        request = self.factory.get('/pay_invoice')
        self.user = AnonymousUser()
        request.user = self.user
        response = pay_invoice(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_manage_admin_page(self):
        request = self.factory.get('/manage_admin')
        self.user = AnonymousUser()
        request.user = self.user
        response = manage_admin(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_create_admin_page(self):
        request = self.factory.get('/create_admin')
        self.user = AnonymousUser()
        request.user = self.user
        response = create_admin(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_delete_admin_page(self):
        request = self.factory.get('/delete_admin')
        self.user = AnonymousUser()
        request.user = self.user
        response = delete_admin(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_update_admin_page(self):
        request = self.factory.get('/update_admin')
        self.user = AnonymousUser()
        request.user = self.user
        response = update_admin(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_promote_admin_page(self):
        request = self.factory.get('/promote_admin')
        self.user = AnonymousUser()
        request.user = self.user
        response = promote_admin(request)
        self.assertEqual(response.status_code, 302)
