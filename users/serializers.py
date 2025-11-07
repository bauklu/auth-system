"""
Сериализаторы для работы с пользователями.
"""

from rest_framework import serializers

from .models import User, Role


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователей.
    """
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'password',
            'confirm_password'
        ]

    def validate(self, data):
        """Проверка пароля."""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        """Создает нового пользователя с хешированным паролем."""
        validated_data.pop("confirm_password")
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения и редактирования данных пользователя.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active']


class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role_name = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(id=data['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        try:
            role = Role.objects.get(name=data['role_name'])
        except Role.DoesNotExist:
            raise serializers.ValidationError("Role not found")
        data['user'] = user
        data['role'] = role
        return data
