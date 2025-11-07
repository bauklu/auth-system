"""
Сериализаторы для проектов.
"""

from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Project.
    """
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "owner",
            "is_active",
            "created_at"
        ]
        read_only_fields = ["id", "owner", "is_active", "created_at"]
