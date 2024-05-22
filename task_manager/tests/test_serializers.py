from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from core.models import Project, Task, Tag
from core.serializers import (
    UserSerializer,
    ProjectSerializer,
    TaskSerializer,
    TagSerializer,
)

User = get_user_model()


class UserSerializerTest(TestCase):

    def test_user_creation(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "newuser@example.com")
        self.assertTrue(user.check_password("newpassword123"))


class ProjectSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )

    def test_project_creation(self):
        data = {
            "name": "New Project",
            "description": "New Description",
            "creator": self.user.id,
        }
        serializer = ProjectSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        project = serializer.save(creator=self.user)
        self.assertEqual(project.name, "New Project")
        self.assertEqual(project.description, "New Description")
        self.assertEqual(project.creator, self.user)


class TaskSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.project = Project.objects.create(
            name="Test Project", description="Test Description", creator=self.user
        )
        self.tag = Tag.objects.create(title="Test Tag")

    def test_task_creation_with_tags(self):
        data = {
            "title": "New Task",
            "description": "New Task Description",
            "project": self.project.id,
            "tags": [self.tag.id],
        }
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        task = serializer.save()
        self.assertEqual(task.title, "New Task")
        self.assertEqual(task.description, "New Task Description")
        self.assertEqual(task.project, self.project)
        self.assertIn(self.tag, task.tags.all())

    def test_task_creation_without_tags(self):
        data = {
            "title": "New Task",
            "description": "New Task Description",
            "project": self.project.id,
            "tags": [],
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("tags", serializer.errors)


class TagSerializerTest(TestCase):

    def test_tag_creation(self):
        data = {"title": "New Tag"}
        serializer = TagSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        tag = serializer.save()
        self.assertEqual(tag.title, "New Tag")
