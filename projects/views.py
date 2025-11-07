"""
Views для работы с проектами (демонстрационные ресурсы).
"""

from rest_framework import generics, permissions

from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsOwnerOrAdmin


class ProjectListCreateView(generics.ListCreateAPIView):
    """
    Позволяет просматривать и создавать проекты.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Возвращает список всех проектов."""
        user = self.request.user

        if user.userrole_set.filter(role__name="admin").exists():
            return Project.objects.filter(is_active=True)

        return Project.objects.filter(owner=user, is_active=True)

    def perform_create(self, serializer):
        """Создает новый проект."""
        serializer.save(owner=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Эндпойнт для просмотра, обновления и мягкого удаления проекта.
    Только для аутентифицированных пользователей,
    которые являются владельцами проекта или админами.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        """Возвращает только активные проекты."""
        return Project.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        """Мягкое удаление: проект становится неактивным."""
        instance.is_active = False
        instance.save()
