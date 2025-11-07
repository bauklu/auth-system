"""
Пользовательские разрешения для приложения projects.

Ограничивают доступ к проектам: только владелец или админ
может изменять или удалять проект.
"""

from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Разрешение: только владелец проекта или администратор.

    Используется для защиты операций обновления и удаления проектов.
    """
    def has_object_permission(self, request, view, obj):
        """
        Возвращает True, если пользователь является администратором
        или владельцем конкретного объекта (проекта).
        """
        user = request.user
        is_admin = (
            hasattr(user, "userrole_set")
            and user.userrole_set.filter(role__name="admin").exists()
        )
        return is_admin or obj.owner == user
