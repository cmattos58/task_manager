from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Project, Task, Tag

User = get_user_model()


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("password123"))


class ProjectModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.project = Project.objects.create(
            name="Test Project", description="Test Description", creator=self.user
        )

    def test_project_creation(self):
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.description, "Test Description")
        self.assertEqual(self.project.creator, self.user)


class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.project = Project.objects.create(
            name="Test Project", description="Test Description", creator=self.user
        )
        self.task = Task.objects.create(
            title="Test Task", description="Test Task Description", project=self.project
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "Test Task Description")
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.status, "PENDING")


class TagModelTest(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(title="Test Tag")

    def test_tag_creation(self):
        self.assertEqual(self.tag.title, "Test Tag")
