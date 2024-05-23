import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import User, Project, Task, Tag


@pytest.mark.django_db
def test_create_user():
    client = APIClient()
    response = client.post(
        reverse('user-list'),
        {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123"
        },
        format='json'
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_obtain_token():
    client = APIClient()
    user = User.objects.create_user(
        username='testuser', email='testuser@example.com', password='testpassword123')
    response = client.post(
        reverse('token_obtain_pair'),
        {
            "username": "testuser",
            "password": "testpassword123"
        },
        format='json'
    )
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_create_project():
    client = APIClient()
    user = User.objects.create_user(
        username='testuser', email='testuser@example.com', password='testpassword123')
    token_response = client.post(
        reverse('token_obtain_pair'),
        {
            "username": "testuser",
            "password": "testpassword123"
        },
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['access'])
    response = client.post(
        reverse('project-list'),
        {
            "name": "Test Project",
            "description": "A test project description"
        },
        format='json'
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Project.objects.count() == 1
    project = Project.objects.get()
    assert project.creator == user


@pytest.mark.django_db
def test_add_members_to_project():
    client = APIClient()
    user = User.objects.create_user(
        username='testuser', email='testuser@example.com', password='testpassword123')
    another_user = User.objects.create_user(
        username='anotheruser', email='anotheruser@example.com', password='testpassword123')
    token_response = client.post(
        reverse('token_obtain_pair'),
        {
            "username": "testuser",
            "password": "testpassword123"
        },
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['access'])
    project_response = client.post(
        reverse('project-list'),
        {
            "name": "Test Project",
            "description": "A test project description"
        },
        format='json'
    )
    project_id = project_response.data['id']
    response = client.patch(
        reverse('project-detail', kwargs={'pk': project_id}),
        {
            "members": [user.id, another_user.id]
        },
        format='json'
    )
    assert response.status_code == status.HTTP_200_OK
    project = Project.objects.get()
    assert user in project.members.all()
    assert another_user in project.members.all()


@pytest.mark.django_db
def test_non_creator_cannot_add_members():
    client = APIClient()
    user = User.objects.create_user(
        username='testuser', email='testuser@example.com', password='testpassword123')
    another_user = User.objects.create_user(
        username='anotheruser', email='anotheruser@example.com', password='testpassword123')
    different_user = User.objects.create_user(
        username='differentuser', email='differentuser@example.com', password='testpassword123')
    token_response = client.post(
        reverse('token_obtain_pair'),
        {
            "username": "testuser",
            "password": "testpassword123"
        },
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['access'])
    project_response = client.post(
        reverse('project-list'),
        {
            "name": "Test Project",
            "description": "A test project description"
        },
        format='json'
    )
    project_id = project_response.data['id']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['access'])
    response = client.patch(
        reverse('project-detail', kwargs={'pk': project_id}),
        {
            "members": [user.id, another_user.id]
        },
        format='json'
    )
    assert response.status_code == status.HTTP_200_OK

    # Different user trying to add members
    different_user_token_response = client.post(
        reverse('token_obtain_pair'),
        {
            "username": "differentuser",
            "password": "testpassword123"
        },
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION='Bearer '
                       + different_user_token_response.data['access'])
    response = client.patch(
        reverse('project-detail', kwargs={'pk': project_id}),
        {
            "members": [different_user.id]
        },
        format='json'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    project = Project.objects.get()
    assert different_user not in project.members.all()


@pytest.mark.django_db
def test_create_task():
    client = APIClient()
    user = User.objects.create_user(
        username='testuser', email='testuser@example.com', password='testpassword123')
    another_user = User.objects.create_user(
        username='anotheruser', email='anotheruser@example.com', password='testpassword123')
    token_response = client.post(
        reverse('token_obtain_pair'),
        {
            "username": "testuser",
            "password": "testpassword123"
        },
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['access'])
    project_response = client.post(
        reverse('project-list'),
        {
            "name": "Test Project",
            "description": "A test project description"
        },
        format='json'
    )
    project_id = project_response.data['id']
    client.patch(
        reverse('project-detail', kwargs={'pk': project_id}),
        {
            "members": [user.id, another_user.id]
        },
        format='json'
    )
    tag = Tag.objects.create(title="Test Tag")
    response = client.post(
        reverse('task-list'),
        {
            "title": "Test Task",
            "description": "A test task description",
            "status": "PENDING",
            "project": project_id,
            "tags": [tag.id]
        },
        format='json'
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.count() == 1
    task = Task.objects.get()
    assert task.project.id == project_id
    assert tag in task.tags.all()


@pytest.mark.django_db
def test_non_member_cannot_create_task():
    client = APIClient()
    user = User.objects.create_user(
        username='testuser', email='testuser@example.com', password='testpassword123')
    another_user = User.objects.create_user(
        username='anotheruser', email='anotheruser@example.com', password='testpassword123')
    token_response = client.post(
        reverse('token_obtain_pair'),
        {
            "username": "testuser",
            "password": "testpassword123"
        },
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response.data['access'])
    project_response = client.post(
        reverse('project-list'),
        {
            "name": "Test Project",
            "description": "A test project description"
        },
        format='json'
    )
    project_id = project_response.data['id']
    tag = Tag.objects.create(title="Test Tag")

    # Another user trying to create task without being a member
    another_user_token_response = client.post(
        reverse('token_obtain_pair'),
        {
            "username": "anotheruser",
            "password": "testpassword123"
        },
        format='json'
    )
    client.credentials(HTTP_AUTHORIZATION='Bearer '
                       + another_user_token_response.data['access'])
    response = client.post(
        reverse('task-list'),
        {
            "title": "Test Task",
            "description": "A test task description",
            "status": "PENDING",
            "project": project_id,
            "tags": [tag.id]
        },
        format='json'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Task.objects.count() == 0
