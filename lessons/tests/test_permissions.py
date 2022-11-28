#from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from lessons.models import User, Request
from lessons.views import feed, home_page, SignUpView, LogInView, update_request
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





class StudentPermissionTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json'
        ]
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(username='johndoe@example.org')
        self.user.save()

    def test_student_access_home_page(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home_page(request)
        self.assertEqual(response.status_code, 200)

        #Will change later to match the code when implemented
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

        #Will change later to match the code when implemented
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

    #Student Update Request View Access already tested in test_update_request_view

class AdminPermissionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('johndoe@example.org',
            first_name='John',
            last_name='Doe',
            password='Password123',
            is_active=True,
            is_admin = True
        )


    def test_admin_access_feed_page(self):
        request = self.factory.get('/feed')
        request.user = self.user
        response = feed(request)
        self.assertEqual(response.status_code, 302)

        #Will change later to match the code when implemented
    def test_admin_access_home_page(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home_page(request)
        self.assertEqual(response.status_code, 200)

        #Will change later to match the code when implemented
    def test_admin_access_log_in_page(self):
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('log_in')
        response = self.client.get(self.url) #follow = true
        #redirect_url = reverse('feed')
        self.assertEqual(response.status_code, 302)
        #Should redirect to admin view
        #self.assertTemplateUsed(response, 'feed.html')

    def test_is_admin_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        self.assertFalse(self.user.is_student, False)
        self.assertTrue(self.user.is_admin, True)
        self.assertFalse(self.user.is_director, False)

        #Will change later to match the code when implemented
    def test_admin_access_sign_up_page(self):
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('sign_up')
        response = self.client.get(self.url) #follow = true
        #redirect_url = reverse('feed')
        self.assertEqual(response.status_code, 302)
        #Should redirect to admin view
        #self.assertTemplateUsed(response, 'feed.html')

    def test_admin_access_update_request_page(self):
        request = self.factory.get('/update_request')
        request.user = self.user
        response = update_request(request)
        self.assertEqual(response.status_code, 302)

class DirectorPermissionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('johndoe@example.org',
            first_name='John',
            last_name='Doe',
            password='Password123',
            is_active=True,
            is_director = True,
        )

    def test_director_access_feed_page(self):
        request = self.factory.get('/feed')
        request.user = self.user
        response = feed(request)
        self.assertEqual(response.status_code, 302)

        #Will change later to match the code when implemented
    def test_director_access_home_page(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home_page(request)
        self.assertEqual(response.status_code, 200)

        #Will change later to match the code when implemented
    def test_director_access_log_in(self):
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('log_in')
        response = self.client.get(self.url) #follow = true
        #redirect_url = reverse('feed')
        self.assertEqual(response.status_code, 302)
        #Should redirect to admin view
        #self.assertTemplateUsed(response, 'feed.html')

    def test_is_director_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        self.assertFalse(self.user.is_student, False)
        self.assertFalse(self.user.is_admin, False)
        self.assertTrue(self.user.is_director, True)

        #Will change later to match the code when implemented
    def test_director_access_sign_up(self):
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse('sign_up')
        response = self.client.get(self.url) #follow = true
        #redirect_url = reverse('feed')
        self.assertEqual(response.status_code, 302)
        #Should redirect to admin view
        #self.assertTemplateUsed(response, 'feed.html')

    def test_director_access_update_request_page(self):
        request = self.factory.get('/update_request')
        request.user = self.user
        response = update_request(request)
        self.assertEqual(response.status_code, 302)
