"""
Маршруты (urls) для приложения users.

Определяют пути к API-эндпойнтам регистрация.
"""

from django.urls import path

from .views import (
    RegisterView,
    UserProfileView,
    DeleteUserView,
    ViewResource,
    AdminUserListView,
    AdminSecretView,
    AssignRoleView,
    ListUserRolesView,
    RemoveRoleView,
    logout_view
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)


urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('logout/', logout_view),
    path('token/refresh/', TokenRefreshView.as_view()),

    # User profile
    path('profile/', UserProfileView.as_view()),
    path('delete/', DeleteUserView.as_view()),

    # Admin part
    path('admin/secret/', AdminSecretView.as_view()),
    path('admin/users/', AdminUserListView.as_view()),
    path('admin/users/roles/', ListUserRolesView.as_view()),
    path('admin/assign-role/', AssignRoleView.as_view()),
    path('admin/remove-role/', RemoveRoleView.as_view()),
    path('api/resource/', ViewResource.as_view(), name='resource'),
]
