from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Project, Task, Tag

User = get_user_model()


class UserViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.client.login(username="testuser", password="password123")

    def test_list_users(self):
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        response = self.client.post(reverse("user-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProjectViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.client.login(username="testuser", password="password123")
        self.project = Project.objects.create(
            name="Test Project", description="Test Description", creator=self.user
        )

    def test_list_projects(self):
        response = self.client.get(reverse("project-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_project(self):
        data = {"name": "New Project", "description": "New Description"}
        response = self.client.post(reverse("project-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Project")


class TaskViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.client.login(username="testuser", password="password123")
        self.project = Project.objects.create(
            name="Test Project", description="Test Description", creator=self.user
        )
        self.project.members.add(self.user)
        self.task = Task.objects.create(
            title="Test Task", description="Test Description", project=self.project
        )

    def test_list_tasks(self):
        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        data = {
            "title": "New Task",
            "description": "New Description",
            "project": self.project.id,
        }
        response = self.client.post(reverse("task-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Task")


class TagViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.client.login(username="testuser", password="password123")
        self.tag = Tag.objects.create(title="Test Tag")

    def test_list_tags(self):
        response = self.client.get(reverse("tag-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_tag(self):
        data = {"title": "New Tag"}
        response = self.client.post(reverse("tag-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Tag")
