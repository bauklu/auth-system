"""
Views для управления пользователями, аутентификацией и ролями.
"""

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import status

from .models import User, UserRole
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    AssignRoleSerializer,
)
from .permissions import IsAdmin, HasPermission


class AdminUserListView(APIView):
    """
    Возвращает список всех пользователей (только для администраторов).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Выводит сериализованный список всех пользователей."""
        if not request.user.userrole_set.filter(role__name="admin").exists():
            return Response(
                {"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN
            )

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    """
    Регистрирует нового пользователя.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Завершает сессию пользователя и помещает refresh-токен в blacklist.
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"detail": "Logout successful"})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Позволяет пользователю просматривать и редактировать свой профиль.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Возвращает данные профиля текущего пользователя."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        """Обновляет профиль текущего пользователя."""
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminSecretView(APIView):
    """
    Пример защищённого эндпойнта.

    Доступен только пользователям с ролью admin.
    Используется для проверки разграничения прав.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Проверка роли."""
        if not request.user.userrole_set.filter(role__name="admin").exists():
            return Response(
                {"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN
            )

        return Response({"secret": "Only admin can see this!"})


class DeleteUserView(APIView):
    """
    Выполняет мягкое удаление пользователя (is_active=False).
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """Деактивирует учетную запись текущего пользователя."""
        user = request.user
        user.is_active = False
        user.save()

        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token not provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as e:
            return Response(
                {"detail": f"Invalid token: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "Account deactivated"},
            status=status.HTTP_200_OK
        )


class ViewResource(APIView):
    """
    Пример защищенного ресурса для проверки прав доступа.
    """
    permission_classes = [HasPermission]
    required_perm = "view_resource"

    def get(self, request):
        """Возвращает демонстрационное сообщение."""
        return Response({"message": "You can view resources!"})


class ListUserRolesView(APIView):
    """Просмотр ролей пользователей (доступно только администратору)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Возвращает роли всех пользователей или одного — по user_id."""
        if not request.user.userrole_set.filter(role__name="admin").exists():
            return Response(
                {"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN
            )

        user_id = request.query_params.get("user_id")
        result = []

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                roles = [ur.role.name for ur in user.userrole_set.all()]
                result.append({
                    "email": user.email,
                    "roles": roles
                })
            except User.DoesNotExist:
                return Response(
                    {"detail": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            for user in User.objects.all():
                roles = [ur.role.name for ur in user.userrole_set.all()]
                result.append({
                    "email": user.email,
                    "roles": roles
                })

        return Response(result, status=status.HTTP_200_OK)


class AssignRoleView(APIView):
    """
    Назначение роли пользователю (только для админа).
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        """
        Присвоение роли пользователю.
        Только администратор может использовать.
        """
        serializer = AssignRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        role = serializer.validated_data['role']

        if not user.is_active:
            return Response(
                {"detail": "Cannot assign role to deactivated user"},
                status=status.HTTP_403_FORBIDDEN
            )

        if UserRole.objects.filter(user=user, role=role).exists():
            message = (
                f"User '{user.email}' already has role "
                f"'{role.name}'"
            )
            return Response(
                {"detail": message}, status=status.HTTP_400_BAD_REQUEST
            )

        UserRole.objects.create(user=user, role=role)
        return Response(
            {"detail": f"Role '{role.name}' assigned to {user.email}"},
            status=status.HTTP_200_OK
        )


class RemoveRoleView(APIView):
    """
    Удаление роли у пользователя (только для администраторов).

    Проверяет, что пользователь активен и имеет указанную роль.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """Удаление роли у пользователя."""
        if not request.user.userrole_set.filter(role__name="admin").exists():
            return Response(
                {"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN
            )

        email = request.data.get("email")
        role_name = request.data.get("role")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user_role = user.userrole_set.filter(role__name=role_name).first()

        if not user_role:
            return Response(
                {"detail": "User does not have this role"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_role.delete()

        return Response({"detail": "Role removed"})
