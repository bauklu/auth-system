# Authentication & Role-Based Access System

  Система аутентификации и разграничения прав доступа на Django REST Framework.

  Позволяет пользователям регистрироваться, авторизовываться, обновлять и удалять профиль, 
  а администраторам — управлять ролями и проектами.

## Функционал

### Аутентификация и управление пользователями
  - Регистрация с валидацией пароля  
  - JWT авторизация (Access / Refresh токены)  
  - Logout с blacklisting токена  
  - Обновление профиля  
  - Мягкое удаление (`is_active=False`)  

### Роли и права
  - Роли: **admin**, **user**  
  - Администратор может:
    - Назначать и снимать роли  
    - Просматривать список пользователей и их ролей  
    - Иметь доступ ко всем проектам  

### Проекты
  - CRUD операции над проектами  
  - Доступ: владелец или администратор

## Установка и запуск
  git clone https://github.com/https://github.com/bauklu/auth_system.git
  cd auth_system
  ### Создание виртуального окружения
    python -m venv venv
    source venv/bin/activate   # или venv\Scripts\activate на Windows
  ### Установка зависимостей
    pip install -r requirements.txt
  
  ### Применение миграций и создание суперпользователя
    python manage.py migrate
    python manage.py createsuperuser
  ### Запуск сервера
    python manage.py runserver

##  Переменные окружения
  Создание .env файла в корне проекта
    SECRET_KEY
    DEBUG
    ALLOWED_HOSTS

## Основные эндпойнты
    POST	  /api/register/	Регистрация
    POST	  /api/login/	Вход (JWT)
    POST	  /api/logout/	Выход
    GET	    /api/profile/	Просмотр профиля
    PUT	    /api/profile/	Обновление профиля
    DELETE	/api/delete/	Мягкое удаление пользователя
    GET	    /api/projects/	Список проектов
    POST	  /api/projects/	Создать проект
    GET	    /api/projects/{id}/	Детали проекта
    PUT	    /api/projects/{id}/	Обновить проект
    DELETE	/api/projects/{id}/	Удалить проект
    POST	  /api/admin/assign-role/	Назначить роль пользователю
    GET	    /api/admin/users/roles/	Список ролей пользователей

## Пример тестовых пользователей:
    Admin   admin@test.com
    User    user@test.com

## Используемые технологии
    Python 3.11+
    Django
    Django REST Framework
    SimpleJWT
    SQLite

## Информация об авторе:

[Баукова Людмила](https://github.com/bauklu)

