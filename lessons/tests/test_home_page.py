from django.test import SimpleTestCase
from django.urls import reverse
from django.http import HttpResponse

class HomePageTest(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_search_by_name(self):
        response = self.client.get(reverse("home_page"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("home_page"))
        self.assertTemplateUsed(response, "home_page.html")
