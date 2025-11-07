"""
Главный файл маршрутизации проекта.

Подключает маршруты приложений users и projects,
а также административную панель Django.
"""

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('projects.urls')),
]
