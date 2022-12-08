#from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from lessons.models import User, Request
from lessons.views import feed, home_page, SignUpView, LogInView, update_request, manage_admin, new_request, pending_requests, new_booking, update_booking, delete_booking, bookings, manage_admin, create_admin, delete_admin, view_invoice, transfers
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

    def test_anonymous_access_bookings_page(self):
        request = self.factory.get('/bookings')
        self.user = AnonymousUser()
        request.user = self.user
        response = bookings(request)
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

    def test_anonymous_access_view_invoice(self):
        request = self.factory.get('/view_invoice')
        self.user = AnonymousUser()
        request.user = self.user
        response = view_invoice(request)
        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_transfers(self):
        request = self.factory.get('/transfers')
        self.user = AnonymousUser()
        request.user = self.user
        response = transfers(request)
        self.assertEqual(response.status_code, 302)

class StudentPermissionTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json'
        ]
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(username='johndoe@example.org')
        self.requestData = Request(
            student=self.user,
            date = '2023-12-12',
            time = '20:20',
            amount=4,
            interval=1,
            duration=30,
            topic="Violin",
            teacher='Mrs.Smith'
        )
        self.requests = Request.objects.filter(student = self.user)


    def test_student_access_home_page(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home_page(request)
        self.assertEqual(response.status_code, 200)

    def test_student_access_log_in(self):
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('log_in')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_is_student_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        self.assertTrue(self.user.is_student, True)
        self.assertFalse(self.user.is_admin, False)
        self.assertFalse(self.user.is_director, False)

    def test_student_access_sign_up(self):
        self.url = reverse('sign_up')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')

    def test_student_access_feed_page(self):
        request = self.factory.get('/feed')
        request.user = self.user
        response = feed(request)
        self.assertEqual(response.status_code, 200)

    def test_student_access_update_request_page(self):
        self.client.login(username=self.user.username, password='Password123')
        self.requestData.save()
        request_url = reverse('update_request', kwargs={'id': self.requests[0].pk})
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)

    def test_student_access_new_request_page(self):
        request = self.factory.get('/new_request')
        request.user = self.user
        response = new_request(request)
        self.assertEqual(response.status_code, 200)

    def test_student_access_bookings_page(self):
        self.client.login(username=self.user.username, password='Password123')
        self.url = reverse('bookings')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_student_access_manage_admin_page(self):
        request = self.factory.get('/manage_admin')
        request.user = self.user
        response = manage_admin(request)
        self.assertEqual(response.status_code, 302)

    def test_student_access_create_admin_page(self):
        request = self.factory.get('/create_admin')
        request.user = self.user
        response = create_admin(request)
        self.assertEqual(response.status_code, 302)

    def test_student_access_delete_admin_page(self):
        request = self.factory.get('/delete_admin')
        request.user = self.user
        response = delete_admin(request)
        self.assertEqual(response.status_code, 302)




class AdminPermissionTestCase(TestCase):
    fixtures = ['lessons/tests/fixtures/default_admin.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(username='petra.pickles@example.org')


    def test_admin_access_feed_page(self):
        request = self.factory.get('/feed')
        request.user = self.user
        response = feed(request)
        self.assertEqual(response.status_code, 200)


    def test_admin_access_home_page(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home_page(request)
        self.assertEqual(response.status_code, 200)

    def test_admin_access_log_in(self):
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('log_in')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')


    def test_is_admin_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        self.assertFalse(self.user.is_student, False)
        self.assertTrue(self.user.is_admin, True)
        self.assertFalse(self.user.is_director, False)

    def test_admin_access_sign_up(self):
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('sign_up')
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    

class DirectorPermissionTestCase(TestCase):
    fixtures = ['lessons/tests/fixtures/default_director.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(username='bobdoe@example.org')
        self.directorList = User.objects.filter(is_director=True)

    def test_director_access_feed_page(self):
        request = self.factory.get('/feed')
        request.user = self.user
        response = feed(request)
        self.assertEqual(response.status_code, 200)

    def test_director_access_home_page(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home_page(request)
        self.assertEqual(response.status_code, 200)

    def test_director_access_log_in(self):
        self.url = reverse('log_in')
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow = True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_is_director_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        self.assertFalse(self.user.is_student, False)
        self.assertTrue(self.user.is_admin, True)
        self.assertTrue(self.user.is_director, True)

    def test_director_access_sign_up(self):
        self.url = reverse('sign_up')
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow = True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_director_access_new_request(self):
        self.url = reverse('new_request')
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow = True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_director_access_update_request(self):
        self.url = reverse('update_request', kwargs={'id': self.directorList[0].pk})
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow = True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_director_access_delete_request(self):
        self.url = reverse('delete_request', kwargs={'id': self.directorList[0].pk})
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow = True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
