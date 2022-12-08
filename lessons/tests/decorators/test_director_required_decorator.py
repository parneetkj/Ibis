from lessons.models import User
from django.test import TestCase
from django.test import RequestFactory
from lessons.decorators import director_required
from django.http import HttpResponse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware

class StudentRequiredTestCase(TestCase):
    fixtures = ['lessons/tests/fixtures/default_director.json',
                'lessons/tests/fixtures/default_admin.json',
                'lessons/tests/fixtures/default_user.json']


    def setUp(self):
        self.user = User.objects.get(username='bobdoe@example.org')
        self.admin = User.objects.get(username='petra.pickles@example.org')
        self.student = User.objects.get(username='johndoe@example.org')
        self.factory = RequestFactory()

    def test_director_successfully_accesses_view(self):
        @director_required
        def a_view(request):
            return HttpResponse()
        request = self.factory.get('/manage_admin')
        request.user = self.user
        response = a_view(request)
        self.assertEqual(response.status_code, 200)

    def test_admin_unsuccessfully_accesses_view(self):
        @director_required
        def a_view(request):
            return HttpResponse()
        request = self.factory.get('/manage_admin')
        request.user = self.admin
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = a_view(request)
        self.assertEqual(response.status_code, 302)

    def test_student_unsuccessful_access_view(self):
        @director_required
        def a_view(request):
            return HttpResponse()
        request = self.factory.get('/manage_admin')
        request.user = self.student
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = a_view(request)
        self.assertEqual(response.status_code, 302)
