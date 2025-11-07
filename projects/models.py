"""
Модели приложения projects.

Описывает структуру данных для проектов: имя, описание, владелец и др.
Связана с пользователями через ForeignKey.
"""

from django.db import models
from django.conf import settings


class Project(models.Model):
    """
    Модель проекта.
    Содержит название, описание, активность, автора.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
