"""
Модели приложения users.

Содержит кастомную модель пользователя, роли и связи между ними.
Используется для управления регистрацией, авторизацией и системой ролей.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """
    Менеджер пользователей.
    Содержит методы для создания обычных пользователей и суперпользователей.
    """
    def create_user(
        self,
        email,
        first_name,
        last_name,
        password=None,
        middle_name=None
    ):
        """Создаёт нового обычного пользователя."""
        if not email:
            raise ValueError("Email required")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """Создаёт суперпользователя с правами администратора."""
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Role(models.Model):
    """Роль пользователя, например 'admin' или 'user'."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    """Права доступа, привязанные к ролям."""
    name = models.CharField(max_length=50)
    codename = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.codename


class UserRole(models.Model):
    """Связь пользователя с ролью."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} — {self.role.name}"


class RolePermission(models.Model):
    """Связь роли с правами доступа."""
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
