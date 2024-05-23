# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.test import APIClient
# from rest_framework import status
# from core.models import User, Project

# class ProjectViewSetTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password')
#         self.project = Project.objects.create(name='Test Project', description='Description', creator=self.user)
#         self.client = APIClient()

#     def test_create_project(self):
#         self.client.force_authenticate(user=self.user)
#         url = reverse('project-list')
#         data = {'name': 'New Project', 'description': 'Description'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
