# from django.test import TestCase
# from django.urls import reverse
# from lessons.models import User, Request

# class DeleteRequestViewTestCase(TestCase):
#     """Test case of delete request view"""
#     fixtures = [
#         'lessons/tests/fixtures/default_user.json',
#     ]

#     def setUp(self):
#         self.user = User.objects.get(username='@johndoe')
#         self.requestData = Request(
#             student=self.user,
#             date = '2023-12-12',
#             time = '20:20',
#             amount=4,
#             interval=1,
#             duration=30,
#             topic="Violin",
#             teacher='Mrs.Smith'
#         )
#         self.requests = Request.objects.filter(student = self.user)

#     def test_delete_request_redirects_correctly(self):
#         self.client.login(email=self.user.email, password='Password123')
#         self.requestData.save()
#         request_url = reverse('delete_request', kwargs={'id': self.requests[0].pk})
#         redirect_url = reverse('feed')
#         response = self.client.get(request_url, follow=True)
#         self.assertRedirects(response, redirect_url,
#             status_code=302, target_status_code=200, fetch_redirect_response=True
#         )
#         self.assertTemplateUsed(response, 'feed.html')
#         messages_list = list(response.context['messages'])
#         self.assertEqual(len(messages_list), 1)

#     def test_delete_request_deletes_correct_request(self):
#         self.client.login(email=self.user.email, password='Password123')
#         self.requestData.save()
#         before_count = Request.objects.count()
#         pk = self.requests[0].pk
#         request_url = reverse('delete_request', kwargs={'id': pk})
#         redirect_url = reverse('feed')
#         response = self.client.get(request_url, follow=True)
#         self.assertRedirects(response, redirect_url,
#             status_code=302, target_status_code=200, fetch_redirect_response=True
#         )
#         after_count = Request.objects.count()
#         self.assertEqual(before_count - 1, after_count)
#         messages_list = list(response.context['messages'])
#         self.assertEqual(len(messages_list), 1)

#         request_url = reverse('update_request', kwargs={'id': pk})
#         redirect_url = reverse('feed')
#         response = self.client.get(request_url, follow=True)
#         self.assertRedirects(response, redirect_url,
#             status_code=302, target_status_code=200, fetch_redirect_response=True
#         )
#         self.assertTemplateUsed(response, 'feed.html')
#         messages_list = list(response.context['messages'])
#         self.assertEqual(len(messages_list), 1)

#     def test_delete_request_redirects_if_not_found(self):
#         self.client.login(email=self.user.email, password='Password123')
#         request_url = reverse('delete_request', kwargs={'id': (Request.objects.count()) +1})
#         redirect_url = reverse('feed')
#         response = self.client.get(request_url, follow=True)
#         self.assertRedirects(response, redirect_url,
#             status_code=302, target_status_code=200, fetch_redirect_response=True
#         )
#         self.assertTemplateUsed(response, 'feed.html')
#         messages_list = list(response.context['messages'])
#         self.assertEqual(len(messages_list), 1)
