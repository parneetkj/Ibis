#from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from lessons.models import User
from lessons.views import feed
from django.contrib.auth.models import AnonymousUser

class AnonymousUserTestCase(TestCase):


    def access_feed_page(self):
        response = self.client.get(reverse("feed"))
        self.assertEqual(response.status_code, 302)



class StudentPermissionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('@johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            password='Password123',
            is_active=True,
            is_student = True
        )

        self.user.save()

    def test_student_access_feed_page(self):
        request = self.factory.get('/feed')
        request.user = self.user
        response = feed(request)
        self.assertEqual(response.status_code, 200)

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
