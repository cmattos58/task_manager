# from django.test import TestCase
# from core.models import User, Project, Task, Tag

# class ProjectModelTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password')
#         self.project = Project.objects.create(name='Test Project', description='Description', creator=self.user)

#     def test_project_creation(self):
#         project = Project.objects.get(id=self.project.id)
#         self.assertEqual(project.name, 'Test Project')
#         self.assertEqual(project.description, 'Description')
#         self.assertEqual(project.creator, self.user)

#     def test_add_member_to_project(self):
#         new_user = User.objects.create_user(username='new_user', email='new@example.com', password='password')
#         self.project.members.add(new_user)
#         self.assertTrue(self.project.members.filter(username='new_user').exists())

# class TaskModelTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password')
#         self.project = Project.objects.create(name='Test Project', description='Description', creator=self.user)
#         self.task = Task.objects.create(title='Test Task', description='Description', project=self.project)

#     def test_task_creation(self):
#         task = Task.objects.get(id=self.task.id)
#         self.assertEqual(task.title, 'Test Task')
#         self.assertEqual(task.description, 'Description')
#         self.assertEqual(task.project, self.project)
