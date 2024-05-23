from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    email = models.EmailField(unique=True)


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(
        User, related_name="created_projects", on_delete=models.CASCADE
    )
    members = models.ManyToManyField(User, related_name="projects")


class Task(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pendente"),
        ("IN_PROGRESS", "Em andamento"),
        ("COMPLETED", "Concluída"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", related_name="tasks")


class Tag(models.Model):
    title = models.CharField(max_length=255)
