# from django.test import TestCase
# from core.models import User, Project, Task, Tag
# from core.serializers import UserSerializer, ProjectSerializer, TaskSerializer, TagSerializer

# class UserSerializerTestCase(TestCase):
#     def test_user_serializer(self):
#         user_data = {'username': 'test_user', 'email': 'test@example.com', 'password': 'password'}
#         serializer = UserSerializer(data=user_data)
#         self.assertTrue(serializer.is_valid())
#         user = serializer.save()
#         self.assertEqual(user.username, 'test_user')

# class ProjectSerializerTestCase(TestCase):
#     def test_project_serializer(self):
#         project_data = {'name': 'Test Project', 'description': 'Description'}
#         serializer = ProjectSerializer(data=project_data)
#         self.assertTrue(serializer.is_valid())
#         project = serializer.save()
#         self.assertEqual(project.name, 'Test Project')

# class TaskSerializerTestCase(TestCase):
#     def test_task_serializer(self):
#         task_data = {'title': 'Test Task', 'description': 'Description'}
#         serializer = TaskSerializer(data=task_data)
#         self.assertTrue(serializer.is_valid())
#         task = serializer.save()
#         self.assertEqual(task.title, 'Test Task')
