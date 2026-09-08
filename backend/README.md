# SQL Battle Backend

Backend API для платформы SQL Battle - интерактивных SQL-соревнований.

## 🛠 Стек технологий

- **FastAPI** - веб-фреймворк
- **SQLAlchemy 2.0** (async) - ORM
- **SQLite** (aiosqlite) - база данных (легко заменить на PostgreSQL)
- **JWT** - аутентификация
- **WebSocket** - реалтайм обновления лидерборда

## 🚀 Быстрый старт

```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Скопировать .env
cp .env.example .env

# 3. Заполнить базу тестовыми данными
python seed.py

# 4. Запустить сервер
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Сервер будет доступен на http://localhost:8000
Документация Swagger: http://localhost:8000/docs

## 📁 Структура проекта

```
backend/
├── main.py              # Точка входа FastAPI
├── config.py            # Конфигурация (env)
├── database.py          # Подключение к БД
├── models.py            # SQLAlchemy модели
├── schemas.py           # Pydantic схемы
├── auth.py              # JWT аутентификация
├── seed.py              # Начальные данные
├── requirements.txt     # Зависимости
├── routers/
│   ├── auth.py          # POST /api/auth/register, /api/auth/login
│   ├── profile.py       # GET /api/profile
│   ├── tasks.py         # GET /api/tasks, POST /api/tasks/{id}/execute, POST /api/tasks/{id}/submit
│   ├── leaderboard.py   # GET /api/leaderboard
│   ├── admin.py         # GET/POST /api/admin/*, GET /api/user/assigned-task
│   └── websocket.py     # WS /ws/leaderboard
└── services/
    └── __init__.py      # SQL sandbox execution
```

## 🔌 API Endpoints

| Метод | URL | Описание |
|-------|-----|----------|
| POST | /api/auth/register | Регистрация |
| POST | /api/auth/login | Вход |
| GET | /api/profile | Профиль пользователя |
| GET | /api/tasks | Список задач |
| GET | /api/tasks/{id} | Детали задачи |
| POST | /api/tasks/{id}/execute | Выполнить SQL (Run) |
| POST | /api/tasks/{id}/submit | Отправить решение |
| GET | /api/leaderboard | Таблица лидеров |
| WS | /ws/leaderboard | Реалтайм лидерборд |
| GET | /api/admin/users | Все пользователи (admin) |
| POST | /api/admin/users/{id}/assign | Назначить задачу |
| POST | /api/admin/users/{id}/clear | Снять назначение |
| GET | /api/admin/tasks | Все задачи (admin) |
| POST | /api/admin/tasks | Создать задачу |
| GET | /api/admin/settings | Настройки |
| PUT | /api/admin/settings | Обновить настройки |
| GET | /api/user/assigned-task | Назначенная задача |

## 🔐 Безопасность

- SQL sandbox: каждый запрос выполняется в изолированной временной БД
- Запрещены: INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE
- Таймаут: 3 секунды
- Только SELECT-запросы
- JWT токены с истечением

## 🔄 Переключение на PostgreSQL

Замените в `.env`:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/sql_battle
```

И установите:
```bash
pip install asyncpg
```
