# Блог-платформа на Django и Django REST Framework

Блог-платформа с API для управления публикациями, комментариями, тегами и лайками. Аутентификация по токенам.

## Эндпоинты API

### Пользователи (Users)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/register/` | Регистрация пользователя, возвращает токен |
| POST | `/api/login/` | Вход, возвращает токен |
| GET | `/api/profile/` | Профиль текущего пользователя (требуется аутентификация) |

### Публикации (Posts)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/posts/` | Список публикаций (пагинация, фильтр по тегу `?tag=slug`, поиск `?search=`) |
| POST | `/api/posts/` | Создание публикации (требуется аутентификация) |
| GET | `/api/posts/{id}/` | Детали публикации |
| PUT | `/api/posts/{id}/` | Обновление (только автор) |
| PATCH | `/api/posts/{id}/` | Частичное обновление (только автор) |
| DELETE | `/api/posts/{id}/` | Удаление (только автор) |
| POST | `/api/posts/{id}/like/` | Поставить лайк (требуется аутентификация) |
| POST | `/api/posts/{id}/unlike/` | Убрать лайк (требуется аутентификация) |

### Комментарии (Comments)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/posts/{post_id}/comments/` | Список комментариев к публикации |
| POST | `/api/posts/{post_id}/comments/` | Добавить комментарий (требуется аутентификация) |
| GET | `/api/posts/{post_id}/comments/{id}/` | Детали комментария |
| PUT | `/api/posts/{post_id}/comments/{id}/` | Обновление (только автор) |
| PATCH | `/api/posts/{post_id}/comments/{id}/` | Частичное обновление (только автор) |
| DELETE | `/api/posts/{post_id}/comments/{id}/` | Удаление (только автор) |

### Теги (Tags)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/tags/` | Список тегов |
| POST | `/api/tags/` | Создание тега (только администратор) |
| GET | `/api/tags/{slug}/` | Детали тега |
| PUT | `/api/tags/{slug}/` | Обновление (только администратор) |
| PATCH | `/api/tags/{slug}/` | Частичное обновление (только администратор) |
| DELETE | `/api/tags/{slug}/` | Удаление (только администратор) |

## Установка

1. Создайте виртуальное окружение:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Создайте базу данных PostgreSQL:

```sql
CREATE DATABASE blog_django;
```

4. Скопируйте `.env.example` в `.env` и настройте переменные окружения:

```bash
copy .env.example .env
```

5. Выполните миграции:

```bash
python manage.py migrate
```

6. Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

## Запуск

```bash
python manage.py runserver
```

Сервер будет доступен по адресу http://127.0.0.1:8000/

## Запуск тестов

При запуске pytest автоматически используется SQLite в памяти, PostgreSQL не требуется.

```bash
pytest
```

Для вывода подробной информации:

```bash
pytest -v
```
