#from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from lessons.models import User, Request
from lessons.views import feed, home_page, sign_up, log_in, update_request
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

class AnonymousUserTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()


    def test_anonymous_access_home_page(self):
        request = self.factory.get('/')
        response = home_page(request)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_access_log_in(self):
        request = self.factory.get('/log_in')
        response = log_in(request)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_access_sign_up(self):
        request = self.factory.get('/sign_up')
        response = sign_up(request)
        self.assertEqual(response.status_code, 200)


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
        self.user = User.objects.get(username='@johndoe')
        self.user.save()

    def test_student_access_home_page(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home_page(request)
        self.assertEqual(response.status_code, 200)

        #Will change later to match the code when implemented
    def test_student_access_log_in(self):
        request = self.factory.get('/log_in')
        request.user = self.user
        response = log_in(request)
        self.assertEqual(response.status_code, 200)

        #Will change later to match the code when implemented
    def test_student_access_sign_up(self):
        request = self.factory.get('/sign_up')
        request.user = self.user
        response = sign_up(request)
        self.assertEqual(response.status_code, 200)

    def test_student_access_feed_page(self):
        request = self.factory.get('/feed')
        request.user = self.user
        response = feed(request)
        self.assertEqual(response.status_code, 200)

    #Student Update Request View Access already tested in test_update_request_view

class AdminPermissionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('@johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
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
        request = self.factory.get('/log_in')
        request.user = self.user
        response = log_in(request)
        self.assertEqual(response.status_code, 200)

        #Will change later to match the code when implemented
    def test_admin_access_sign_up_page(self):
        request = self.factory.get('/sign_up')
        request.user = self.user
        response = sign_up(request)
        self.assertEqual(response.status_code, 200)

    def test_admin_access_update_request_page(self):
        request = self.factory.get('/update_request')
        request.user = self.user
        response = update_request(request)
        self.assertEqual(response.status_code, 302)

class DirectorPermissionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('@johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
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
        request = self.factory.get('/log_in')
        request.user = self.user
        response = log_in(request)
        self.assertEqual(response.status_code, 200)

        #Will change later to match the code when implemented
    def test_director_access_sign_up(self):
        request = self.factory.get('/sign_up')
        request.user = self.user
        response = sign_up(request)
        self.assertEqual(response.status_code, 200)

    def test_director_access_update_request_page(self):
        request = self.factory.get('/update_request')
        request.user = self.user
        response = update_request(request)
        self.assertEqual(response.status_code, 302)
