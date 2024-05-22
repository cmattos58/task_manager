from rest_framework import serializers
from .models import User, Project, Task, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("creator",)


class TaskSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if not data["tags"]:
            raise serializers.ValidationError("Todas as tarefas devem ter tags.")
        return data

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("created_at",)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
