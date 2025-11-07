"""
Пользовательские классы разрешений (permissions) для приложения users.

"""

# from rest_framework.permissions import BasePermission
from rest_framework import permissions

from users.models import UserRole, RolePermission


class IsAdmin(permissions.BasePermission):
    """
    Позволяет доступ только пользователям с ролью 'admin'.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.userrole_set.filter(role__name="admin").exists()


class HasPermission(permissions.BasePermission):
    """
    Проверяет доступ пользователя на основе его ролей и разрешений.

    Пользователь должен быть аутентифицирован, а его роли —
    содержать разрешение с codename, равным `required_perm`.
    """
    required_perm = None

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        roles = UserRole.objects.filter(
            user=request.user).values_list('role', flat=True)
        perms = RolePermission.objects.filter(
            role_id__in=roles).values_list('permission__codename', flat=True)

        return self.required_perm in perms
