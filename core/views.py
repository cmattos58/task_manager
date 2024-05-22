from rest_framework import viewsets, permissions, status
from .models import User, Project, Task, Tag
from .serializers import (
    UserSerializer,
    ProjectSerializer,
    TaskSerializer,
    TagSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.creator != request.user:
            raise PermissionDenied("Você não tem permissão para editar este projeto.")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.creator != request.user:
            raise PermissionDenied("Você não tem permissão para excluir este projeto.")
        return super().destroy(request, *args, **kwargs)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]
        if not project.members.filter(id=self.request.user.id).exists():
            raise PermissionDenied(
                "Você não tem permissão para criar tarefas neste projeto."
            )
        serializer.save(project=project)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == "COMPLETED":
            raise PermissionDenied("Tarefas concluídas não podem ser editadas.")
        return super().update(request, *args, **kwargs)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
